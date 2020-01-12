# Introduction

The function of this application is simply to turn a colorful image to a black and white one and then recolorize it back to colorful into a video.

## Demo

![https://im2.ezgif.com/tmp/ezgif-2-d6b8a6438639.gif](https://im2.ezgif.com/tmp/ezgif-2-d6b8a6438639.gif)

## Requirements

`pipenv Python 3.7 Flask PIL`

### Environment variables

**_GOOGLE_APPLICATION_CREDENTIALS_**

If you want to upload the files to your google cloud storage, you'll have to create a service account and set environment variable to that service account json file path.

**_DEBUG_**

This environment variable is needed if you'll be running this application on your local computer.

**_BUCKET_NAME_**

Set this only if you're planning to run this on production or when you want to upload your final product to google cloud storage.

## Run the program

```bash
pipenv install

pipenv shell

DEBUG=1 python main.py
```

## Docker

I'll create a docker image for this later, or if you feel like it - make a pull request and contribute 😍💯
