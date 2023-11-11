#!/bin/bash

# Download ffmpeg.exe from S3
wget -O ffmpeg.exe https://privatevideotranslation.s3.us-west-1.amazonaws.com/ffmpeg.exe

# Add the directory to PATH
export PATH="/app:$PATH"