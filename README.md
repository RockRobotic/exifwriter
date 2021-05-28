# Rock Robotic Image Exif Writer

## Instructions

Dowload zip file from the latest release https://github.com/RockRobotic/exifwriter/releases.

Unzip and navigate to the 'dist' folder and run the exifwrite program.

Select the csv file created by PCPainter and the folder containing your camera images and click start. GPS data will be written to the photos in the folder you selected. If you do not have the csv file, then a less accurate method can be used by selecting the trajectory file intead. NOTE: the csv file processing is preferred.

## Compatibility

Windows 10 distribution included. However, this can be run with any computer which has python 3.7+ by running:

`pip install Gooey piexif`

`python exifwrite.py`

## Development

conda create --name exifwriter python=3.8.3

pip install Gooey piexif pyinstaller pyproj

pyinstaller --noconsole --onefile --windowed exifwrite.py
