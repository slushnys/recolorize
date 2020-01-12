from PIL import ImageEnhance, Image
import imageio
import numpy as np
from uuid import uuid4
from gcloud import storage
import os

from flask import Flask, request, render_template, send_file

# 1 fps ~7s
# 2 fps ~13s
# 3 fps ~16s # I think its the most optimal for quality and time it took. Good server would probably take less than 10s.
# 4 fps ~22s
# 5 fps ~27.35s
# 10 fps ~53.48s
# 15 fps ~75s
# 24 fps ~106s

"""
Square Image: 1080px in width by 1080px in height

Vertical Image:  1080px in width by 1350px in height

Horizontal Image: 1080px in width by 566px in height
"""

DEBUG = os.getenv('DEBUG', False)
BUCKET_NAME = os.getenv('BUCKET_NAME', 'slushnys')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


def open_and_resize_image(input):
    img = Image.open(input)

    max_height = 1344
    max_width = 1080

    if img.height > max_height and img.height > img.width:
        # vertical image
        percentage_decrease = (max_height * 100) / img.height / 100
        new_height = round(img.height * percentage_decrease)
        new_width = round(img.width * percentage_decrease)
        img = img.resize((new_width, new_height))

    if (img.width > max_width and img.width > img.height) or (img.width == img.height and img.width > max_width):
        # Horizontal image
        percentage_decrease = (max_width * 100) / img.width / 100
        new_height = round(img.height * percentage_decrease)
        new_width = round(img.width * percentage_decrease)
        img = img.resize((new_width, new_height))

    return img


def process(is_local, input, output, seconds=5, fps=3):
    extra_duration = 5 * fps

    total_frames = seconds * fps
    color_percentage_for_each_frame = (
        100 / total_frames) / 100  # for the 0. mark

    im = open_and_resize_image(input)

    # imageio.RETURN_BYTES
    write_to = '<bytes>'
    if is_local:
        write_to = 'output/{}.mp4'.format(output)

    writer = imageio.get_writer(write_to, format='mp4', mode='I', fps=fps)
    for i in range(total_frames + extra_duration):
        if i < total_frames:
            processed = ImageEnhance.Color(im).enhance(
                color_percentage_for_each_frame * i)
            writer.append_data(np.asarray(processed))
        else:
            writer.append_data(np.asarray(im))
    writer.close()
    if not is_local:
        # Configuration to add videos to google cloud.
        client = storage.Client()
        client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
        bucket = client.get_bucket(BUCKET_NAME)

        blob = bucket.blob('{}.mp4'.format(output))
        saved_file = writer.request.get_result()
        blob.upload_from_string(saved_file)
        print('blob name', blob.name)
        return blob.name
    else:
        return write_to


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            return render_template('index.html', error="You haven't uploaded a file")
        output = uuid4()
        file = process(DEBUG, f, output, 5, 24)
        print(DEBUG)
        if DEBUG:
            return send_file(file, mimetype='video/mp4', as_attachment=True)
        else:
            return render_template('upload_successful.html', is_local=DEBUG, file=file)
    else:

        return render_template('./index.html')


if __name__ == '__main__':
    app.run(debug=DEBUG)
