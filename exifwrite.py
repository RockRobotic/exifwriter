#!/usr/bin/env python

import glob
import os
import csv
import piexif
from fractions import Fraction
from gooey import Gooey
from gooey import GooeyParser

@Gooey(progress_regex=r"^progress: (?P<current>\d+)/(?P<total>\d+)$",
       progress_expr="current / total * 100")

def main():
    # Initialize parser
    parser = GooeyParser(description="Rock Robotic Exif Writer")
    parser.add_argument(
        'trajectory',
        metavar='Trajectory File',
        help='Trajectory File',
        widget='FileChooser'
    )
    parser.add_argument(
        'base_camera_dir',
        metavar='Photo Directory',
        help="Photo Directory",
        widget='DirChooser')

    # Read arguments from command line
    args = parser.parse_args()
    photos = glob.glob(args.base_camera_dir + os.sep + '*jpg')

    traj = open(args.trajectory, newline='')
    trajectory_csv = csv.reader(traj, delimiter='\t')
    total_photos = len(photos)
    photo_num = 0
    for photo in photos:
        head, tail = os.path.split(photo)
        name = tail.split('_')
        startTime = name[1]
        name2 = name[2].split('.')

        imageStart = (int(startTime) % 604800000000) / 1000000
        i = 0
        before = ''
        after = ''
        previous = ''
        traj.seek(0)
        for line in trajectory_csv:
            if i > 0:
                if imageStart < float(line[1]):
                    if after == '':
                        before = previous
                        after = line
                        break

                previous = line

            i = i + 1

        if before != '' and after != '':
            # Find which one is closest.
            beforeDiff = float(before[1]) - imageStart
            afterDiff = imageStart - float(after[1])
            if beforeDiff < afterDiff:
                set_gps_location(photo, float(before[4]), float(before[3]), float(before[5]))
            else:
                set_gps_location(photo, float(after[4]), float(after[3]), float(after[5]))
        photo_num = photo_num + 1
        print('progress: ' + str(photo_num) + '/' + str(total_photos))

def to_deg(value, loc):
    """convert decimal coordinates into degrees, munutes and seconds tuple
    Keyword arguments: value is float gps-value, loc is direction list ["S", "N"] or ["W", "E"]
    return: tuple like (25, 13, 48.343 ,'N')
    """
    if value < 0:
        loc_value = loc[0]
    elif value > 0:
        loc_value = loc[1]
    else:
        loc_value = ""
    abs_value = abs(value)
    deg =  int(abs_value)
    t1 = (abs_value-deg)*60
    min = int(t1)
    sec = round((t1 - min)* 60, 5)
    return (deg, min, sec, loc_value)


def change_to_rational(number):
    """convert a number to rantional
    Keyword arguments: number
    return: tuple like (1, 2), (numerator, denominator)
    """
    f = Fraction(str(number))
    return (f.numerator, f.denominator)


def set_gps_location(file_name, lat, lng, altitude):
    """Adds GPS position as EXIF metadata
    Keyword arguments:
    file_name -- image file
    lat -- latitude (as float)
    lng -- longitude (as float)
    altitude -- altitude (as float)
    """
    lat_deg = to_deg(lat, ["S", "N"])
    lng_deg = to_deg(lng, ["W", "E"])

    exiv_lat = (change_to_rational(lat_deg[0]), change_to_rational(lat_deg[1]), change_to_rational(lat_deg[2]))
    exiv_lng = (change_to_rational(lng_deg[0]), change_to_rational(lng_deg[1]), change_to_rational(lng_deg[2]))

    gps_ifd = {
        piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
        piexif.GPSIFD.GPSAltitudeRef: 1,
        piexif.GPSIFD.GPSAltitude: change_to_rational(round(altitude)),
        piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
        piexif.GPSIFD.GPSLatitude: exiv_lat,
        piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
        piexif.GPSIFD.GPSLongitude: exiv_lng,
    }

    gps_exif = {"GPS": gps_ifd}

    # get original exif data first!
    exif_data = piexif.load(file_name)

    # update original exif data to include GPS tag
    exif_data.update(gps_exif)
    exif_bytes = piexif.dump(exif_data)

    piexif.insert(exif_bytes, file_name)

if __name__ == '__main__':
    main()