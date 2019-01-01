import urllib.request
import sys
import time
from os import path
from seriesdw import utility
import argparse


def arguments():
    """Parse the arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('URL', help="URL of the file",
                        default=None, type=str)
    parser.add_argument('des', help="The name of the file\
                        to be saved with.", default=None, nargs='?')

    args = parser.parse_args()
    return args


def get_name(URL):
    """Try to get the name of the file from the URL."""
    name = 'temp'

    temp_url = URL

    split_url = temp_url.split('/')

    for name in split_url[::-1]:
        if name != '':
            break

    return name


def format_size(size):
    """Format the passed size.

    If its more than an 1 Mb then return the size in Mb's
    else return it in Kb's along with the unit.
    """
    formatted_size = size
    dw_unit = 'bytes'

    if formatted_size > (1024 * 1024 * 1024):
        formatted_size = size / (1024 * 1024 * 1024)
        dw_unit = "GB's"
    elif formatted_size > (1024 * 1024):
        formatted_size = size / (1024 * 1024)
        dw_unit = "MB's"
    elif formatted_size > 1024:
        formatted_size = size / 1024
        dw_unit = "kb's"

    return (formatted_size, dw_unit)



def download(url, des=None):
    try:
        # Check if the des is passed
        if des is not None:
            if path.isdir(des):
                des = path.join(des, get_name(url))
        else:
            des = get_name(URL)

        # Download files with a progressbar showing the percentage
        try:
            u = urllib.request.urlopen(url)
        except Exception as e:
            print("ERROR: {}".format(e))
            return False
        f = open(des, 'wb')
        meta = u.info()

        file_size = None
        try:
            file_size = int(meta["Content-Length"])
            formatted_file_size, dw_unit = format_size(file_size)
            print("Size: {} {}".format(round(formatted_file_size), dw_unit))
            print("Saving as: {}".format(des))
        except TypeError:
            pass

        file_size_dl = 0
        block_sz = 8192

        beg_time = time.time()
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            # Initialize all the variables that cannot be calculated
            # to ''
            speed = ''
            time_left = ''
            time_unit = ''
            percent = ''

            if file_size is not None:
                # Calculate speed
                speed = (file_size_dl / 1024) / (time.time() - beg_time)

                # Calculate time left
                time_left = round(((file_size - file_size_dl) / 1024) / speed)
                time_unit = 's'

                # Convert to min or hours as req
                if time_left > 3600:
                    time_left = round(time_left / 3600)
                    time_unit = 'h'
                elif time_left > 60:
                    time_left = round(time_left / 60)
                    time_unit = 'm'

                # Calculate percentage
                percent = file_size_dl * 100 / file_size

            # file_size to show
            file_size_to_disp, dw_unit = format_size(file_size_dl)

            # Basename
            basename = path.basename(des)

            # Calculate amount of space req in between
            length = utility.get_terminal_length()

            stuff_len = len(basename) + 13 + 17 + 7 + 26 + 3
            space = 0

            if stuff_len < length:
                space = length - stuff_len
            elif stuff_len > length:
                basename = basename[:(length - stuff_len) - 2] + '..'

            if file_size is not None:
                status = r"%s %s %0.2f %s |%d kbps| ETA: %s %s |%-20s| |%3.2f%%|" % (basename, space * " ", file_size_to_disp, dw_unit, speed, time_left, time_unit, "-" * int(percent / 5), percent)
            else:
                status = r"%s %s %0.2f %s" %(basename, space * " ", file_size_to_disp, dw_unit)
            sys.stdout.write('\r')
            sys.stdout.write(status)
            sys.stdout.flush()

        f.close()

        print()
        return True
    except Exception as e:
        print("ERROR: {}".format(e))
        return False


if __name__ == "__main__":
    args = arguments()
    download(args.URL, args.des)
