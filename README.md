# Rock Robotic Image Exif Writer

## Instructions

Dowload zip file from the latest release https://github.com/RockRobotic/exifwriter/releases.

Unzip and navigate to the 'dist' folder and run the exifwrite program.

Select your trajectory file and the folder containing your camera images and click start. GPS data will be written to the photos in the folder you selected.

## Compatibility

Windows 10 distribution included. However, this can be run with any computer which has python 3.7+ by running:

`pip install Gooey piexif`

`python exifwrite.py`

## Development

pip install Gooey piexif pyinstaller

pyinstaller --noconsole --onefile --windowed exifwrite.py