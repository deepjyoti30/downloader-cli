#!/usr/bin/env python3

import urllib.request
import sys
import time
from os import path, get_terminal_size, name
import argparse
import itertools
from re import match

from downloader_cli.__version__ import __version__

# import traceback ## Required to debug at times.


def arguments():
    """Parse the arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('URL', help="URL of the file",
                        type=str, metavar="SOURCE")
    parser.add_argument('des', help="target filepath (existing directories \
                        will be treated as the target location)", default=None, nargs="?",
                        metavar='TARGET')
    force = parser.add_mutually_exclusive_group()
    force.add_argument('-f', '-o', '--force', help="overwrite if the file already exists",
                       action="store_true")
    force.add_argument('-c', '--resume', help='resume failed or cancelled \
                        download (partial sanity check)', action="store_true")
    parser.add_argument('-e', '--echo', help="print the filepath to stdout after \
                        downloading (other output will be redirected \
                        to stderr)", action="store_true")
    parser.add_argument(
        '-q', '--quiet', help="suppress filesize and progress info", action="store_true")
    parser.add_argument(
        '-b', '--batch', help="Download files in batch. If this flag is passed \
        the passed source will be considered as a file with download links \
        seperated by a newline. This flag will be ignored if source is a valid \
        URL.", default=False, action="store_true"
    )
    parser.add_argument('-v', '--version', action='version',
                        version=__version__,
                        help='show the program version number and exit')

    args = parser.parse_args()
    return args


class Download:

    def __init__(
        self,
        URL,
        des=None,
        overwrite=False,
        continue_download=False,
        echo=False,
        quiet=False,
        batch=False,
        icon_done="▓",
        icon_left="░",
        icon_border="|"
    ):
        self.URL = URL
        self.des = des
        self.passed_dir = None
        self.headers = {}
        self.f_size = 0
        self.done_icon = icon_done if len(icon_done) < 2 else "▓"
        self.left_icon = icon_left if len(icon_left) < 2 else "░"
        self.border_left, self.border_right = self._extract_border_icon(
            icon_border)
        self._cycle_bar = None
        self.echo = echo
        self.quiet = quiet
        self.batch = batch
        self.overwrite = overwrite
        self.continue_download = continue_download
        self.file_exists = False
        self.ostream = sys.stderr if self.echo else sys.stdout

    def _extract_border_icon(self, passed_icon):
        """"
        Extract the passed border icon according to
        what is passed.

        If the string has length equal to 2, then use the
        first char as left border icon and the second as
        right.

        If the string has length equal to 1, use the same icon for both.
        """
        if len(passed_icon) == 1:
            return passed_icon, passed_icon

        if len(passed_icon) == 2:
            return passed_icon[0], passed_icon[1]

        return "|", "|"

    def _build_headers(self, rem):
        """Build headers according to requirement."""
        self.headers = {"Range": "bytes={}-".format(rem)}
        print("Trying to resume download at: {} bytes".format(
            rem), file=self.ostream)

    def _parse_exists(self):
        """This function should be called if the file already exists.

        In that case there are two possibilities, it's partially downloaded
        or it's a proper file.
        """
        if self.overwrite:
            return
        elif self.continue_download:
            cur_size = path.getsize(self.des)
            original_size = urllib.request.urlopen(self.URL).info()[
                'Content-Length']

            if original_size is None:
                print("WARNING: Could not perform sanity check on partial download.",
                      file=self.ostream)
                self._build_headers(cur_size)
            elif cur_size < int(original_size):
                self._build_headers(cur_size)
        else:
            print("ERROR: File exists. See 'dw --help' for solutions.",
                  file=self.ostream)
            exit(-1)

    def _preprocess_conn(self):
        """Make necessary things for the connection."""
        self.req = urllib.request.Request(url=self.URL, headers=self.headers)

        try:
            self.conn = urllib.request.urlopen(self.req)
        except Exception as e:
            print("ERROR: {}".format(e))
            exit()

        self.f_size = self.conn.info()['Content-Length']

        if self.f_size is not None:
            self.f_size = int(self.f_size)

    def _get_terminal_length(self):
        """Return the length of the terminal."""
        # If quiet is passed, skip this calculation and return a default length
        if self.quiet:
            return 50

        cols = get_terminal_size().columns
        return cols if name != "nt" else cols - 1

    def _parse_destination(self):
        # Check if the des is passed
        if self.des is not None:
            if path.isdir(self.des):
                self.passed_dir = self.des
                self.des = path.join(self.des, self._get_name())
        else:
            self.des = self._get_name()

        # Put a check to see if file already exists.
        # Try to resume it if that's true
        if path.exists(self.des):
            self._parse_exists()
            self.file_exists = True

    def _is_valid_src_path(self, file_path):
        """Check to see if the path passed is
        a valid source path.

        A valid source path would be a file that
        is not a directory and actually a file
        present in the disk.
        """
        return not path.exists(file_path) or not path.isfile(file_path)

    def _parse_URL(self):
        """
        The URL can be a file as well so in that case we
        will download each URL from that file.

        In case the URL is not a file and just a simple URL,
        download just that one.

        returns: A list of urls
        """
        if match(r"^https?://*|^file://*", self.URL):
            return [self.URL]

        # Below code will only be executed if the -b
        # flag is passed
        if not self.batch:
            print("{}: not a valid URL. Pass -b if it is a file "
                  "containing various URL's and you want bulk download."
                  .format(self.URL))
            exit(0)

        rel_path = path.expanduser(self.URL)

        # Put a check to see if the file is present
        if self._is_valid_src_path(rel_path):
            print("{}: not a valid name or is a directory".format(rel_path))
            exit(-1)

        # If it's not an URL, read the contents.
        # Since the URL is not an actual URL, we're assuming
        # it is a file that contains URL's seperated by new
        # lines.
        with open(rel_path, "r") as RSTREAM:
            return RSTREAM.read().split("\n")

    def _get_name(self):
        """Try to get the name of the file from the URL."""

        name = 'temp'
        temp_url = self.URL

        split_url = temp_url.split('/')[-1]

        if split_url:
            # Remove query params if any
            name = split_url.split("?")[0]

        return name

    def _format_size(self, size):
        """Format the passed size.

        If its more than an 1 Mb then return the size in Mb's
        else return it in Kb's along with the unit.
        """
        map_unit = {0: 'bytes', 1: "KB", 2: "MB", 3: "GB"}
        formatted_size = size

        no_iters = 0
        while formatted_size > 1024:
            no_iters += 1
            formatted_size /= 1024

        return (formatted_size, map_unit[no_iters])

    def _format_time(self, time_left):
        """Format the passed time depending."""
        unit_map = {0: 's', 1: 'm', 2: 'h', 3: 'd'}

        no_iter = 0
        while time_left > 60:
            no_iter += 1
            time_left /= 60

        return time_left, unit_map[no_iter]

    def _format_speed(self, speed):
        """Format the speed."""
        unit = {0: 'Kb/s', 1: 'Mb/s', 2: 'Gb/s'}

        inc_with_iter = 0
        while speed > 1000:
            speed = speed / 1000
            inc_with_iter += 1

        return speed, unit[inc_with_iter]

    def _get_speed_n_time(self, file_size_dl, beg_time, cur_time):
        """Return the speed and time depending on the passed arguments."""

        # Sometimes the beg_time and the cur_time are same, so we need
        # to make sure that doesn't raise a ZeroDivisionError in the
        # following line.
        if cur_time == beg_time:
            return "Inf", "", 0, ""

        # Calculate speed
        speed = (file_size_dl / 1024) / (cur_time - beg_time)

        # Calculate time left
        if self.f_size is not None:
            time_left = ((self.f_size - file_size_dl) / 1024) / speed
            time_left, time_unit = self._format_time(time_left)
        else:
            time_left, time_unit = 0, ""

        # Format the speed
        speed, s_unit = self._format_speed(speed)

        return round(speed), s_unit, round(time_left), time_unit

    def _get_pos(self, reduce_with_each_iter):
        if self._cycle_bar is None:
            self._cycle_bar = itertools.cycle(
                range(0, int(reduce_with_each_iter)))

        return (next(self._cycle_bar) + 1)

    def _get_bar(self, status, length, percent=None):
        """Calculate the progressbar depending on the length of terminal."""

        map_bar = {
            40: r"|%-40s|",
            20: r"|%-20s|",
            10: r"|%-10s|",
            5: r"|%-5s|",
            2: r"|%-2s|"
        }
        # Till now characters present is the length of status.
        # length is the length of terminal.
        # We need to decide how long our bar will be.
        cur_len = len(status) + 2  # 2 for bar

        if percent is not None:
            cur_len += 5  # 5 for percent

        reduce_with_each_iter = 40
        while reduce_with_each_iter > 0:
            if cur_len + reduce_with_each_iter > length:
                reduce_with_each_iter = int(reduce_with_each_iter / 2)
            else:
                break

        # Add space.
        space = length - (len(status) + 2 + reduce_with_each_iter + 5)
        status += r"%s" % (" " * space)

        if reduce_with_each_iter > 0:
            # Make BOLD
            status += "\033[1m"
            # Add color.
            status += "\033[1;34m"
            if percent is not None:
                done = int(percent / (100 / reduce_with_each_iter))
                status += r"%s%s%s%s" % (
                    self.border_left,
                    self.done_icon * done,
                    self.left_icon * (reduce_with_each_iter - done),
                    self.border_right)
            else:
                current_pos = self._get_pos(reduce_with_each_iter)
                bar = " " * (current_pos - 1) if current_pos > 1 else ""
                bar += self.done_icon * 1
                bar += " " * int((reduce_with_each_iter) - current_pos)
                status += r"%s%s%s" % (self.border_left,
                                       bar, self.border_right)

        status += "\033[0m"
        return status

    def _download(self):
        try:
            self._parse_destination()

            # Download files with a progressbar showing the percentage
            self._preprocess_conn()
            WSTREAM = open(self.des, 'ab')

            if self.f_size is not None and self.quiet is False:
                formatted_file_size, dw_unit = self._format_size(self.f_size)
                print("Size: {} {}".format(
                    round(formatted_file_size), dw_unit), file=self.ostream)

            _owrite = ("Overwriting: {}" if (self.file_exists and
                                             self.overwrite) else "Saving as: {}").format(self.des)
            if self.quiet:
                self.ostream.write(_owrite)
                self.ostream.write("...")
            else:
                print(_owrite, file=self.ostream)
                self.ostream.flush()

            file_size_dl = 0
            block_sz = 8192

            beg_time = time.time()
            while True:
                buffer = self.conn.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                WSTREAM.write(buffer)

                # Initialize all the variables that cannot be calculated
                # to ''
                speed = ''
                time_left = ''
                time_unit = ''
                percent = ''

                speed, s_unit, time_left, time_unit = self._get_speed_n_time(
                    file_size_dl,
                    beg_time,
                    cur_time=time.time()
                )

                if self.f_size is not None:
                    percent = file_size_dl * 100 / self.f_size

                # Get basename
                self.basename = path.basename(self.des)

                # Calculate amount of space req in between
                length = self._get_terminal_length()

                f_size_disp, dw_unit = self._format_size(file_size_dl)

                status = r"%-7s" % ("%s %s" % (round(f_size_disp), dw_unit))
                status += r"| %-3s %s " % ("%s" % (speed), s_unit)

                if self.f_size is not None:
                    status += r"|| ETA: %-4s " % ("%s %s" %
                                                  (time_left, time_unit))
                    status = self._get_bar(status, length, percent)
                    status += r" %-4s" % ("{}%".format(round(percent)))
                else:
                    status = self._get_bar(status, length)

                if not self.quiet:
                    self.ostream.write('\r')
                    self.ostream.write(status)
                    self.ostream.flush()

            WSTREAM.close()
            if self.quiet:
                self.ostream.write("...success\n")
                self.ostream.flush()
            return True
        except KeyboardInterrupt:
            self.ostream.flush()
            print("Keyboard Interrupt passed. Exiting peacefully.")
            exit(0)
        except Exception as e:
            print("ERROR: {}".format(e))
            return False

    def download(self):
        """
        download will iterate through a list of possible url's
        and destinations and keep passing to the actual download
        method _download().
        """
        urls = self._parse_URL()
        for url in urls:
            self.URL = url
            self._download()
            self.des = self.passed_dir


def main():
    args = arguments()
    _out = Download(URL=args.URL, des=args.des, overwrite=args.force,
                    continue_download=args.resume, echo=args.echo,
                    quiet=args.quiet, batch=args.batch)
    success = _out.download()
    if success and args.echo:
        print(_out.des)
    sys.stderr.close


if __name__ == "__main__":
    main()
