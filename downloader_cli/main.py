import argparse
import sys

from downloader_cli.__version__ import __version__
from downloader_cli.download import Download


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

    ui_group = parser.add_argument_group("UI Group")
    ui_group.add_argument(
        "--done", help="Icon indicating the percentage done of the downloader", type=str, default=None
    )
    ui_group.add_argument(
        "--left", help="Icon indicating the percentage remaining to download", type=str, default=None
    )
    ui_group.add_argument(
        "--current", help="Icon indicating the current percentage in the progress bar", type=str, default=None
    )
    ui_group.add_argument(
        "--color-done", help="Color for the done percentage icon", type=str, default=""
    )
    ui_group.add_argument(
        "--color-left", help="Color for the remaining percentage icon", type=str, default=""
    )
    ui_group.add_argument(
        "--color-current", help="Color for the current indicator icon in the progress bar", type=str, default=""
    )
    ui_group.add_argument(
        "--icon-border", help="Icon for the border of the progress bar", type=str, default="|"
    )

    args = parser.parse_args()
    return args


def main():
    args = arguments()
    _out = Download(URL=args.URL, des=args.des, overwrite=args.force,
                    continue_download=args.resume, echo=args.echo,
                    quiet=args.quiet, batch=args.batch, icon_done=args.done,
                    icon_left=args.left, color_done=args.color_done,
                    color_left=args.color_left, icon_border=args.icon_border,
                    icon_current=args.current, color_current=args.color_current)
    success = _out.download()
    if success and args.echo:
        print(_out.des)
    sys.stderr.close


if __name__ == "__main__":
    main()
