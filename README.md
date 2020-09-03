<h1 align="center">downloader-cli</h1>
<h3 align="center">A simple downloader written in Python with an awesome progressbar.</h3>

<div align="center" style="padding-top: 2em !important; padding-bottom: 2em; !important">
    <img src=".github/dw.gif">
</div>

<div align="center">
<br/>

<a href="#installation">Installation</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#requirements">Requirements</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#usage">Usage</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#use-it">Use It</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#other-examples">Other examples</a>&nbsp;&nbsp;&nbsp;
<br/><br/>

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)<br/><br/>
[![License](https://img.shields.io/badge/License-MIT-pink.svg?style=for-the-badge)](LICENSE) [![Downloads](https://img.shields.io/badge/dynamic/json?style=for-the-badge&maxAge=86400&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fdownloader-cli)](https://img.shields.io/badge/dynamic/json?style=for-the-badge&maxAge=86400&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fdownloader-cli) ![PyPI](https://img.shields.io/pypi/v/downloader-cli?style=for-the-badge) ![AUR](https://img.shields.io/aur/version/downloader-cli?style=for-the-badge) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-purple.svg?style=for-the-badge)](http://makeapullrequest.com)

</div>

# Installation

- [PyPI](#pypi)
- [Arch](#arch)
- [Gentoo](#gentoo)
- [Manual](#manual)

>NOTE: The following packages (except installing manually) will get you the latest release. If you want to try out the latest development stuff, install manually.

### PyPI

The package is available in PyPI [here](https://pypi.org/project/downloader-cli/)

Install it using

```sh
pip install downloader-cli
```

### Arch

The package is available in the AUR [here](https://aur.archlinux.org/packages/downloader-cli/)

Install it using `yay`

```console
yay -S downloader-cli
```

### Gentoo

The package is also available in src_prepare Gentoo overlay [here](https://gitlab.com/src_prepare/src_prepare-overlay/-/tree/master/net-misc/downloader-cli/)

First set up src_prepare-overlay

```sh
sudo emerge -anv --noreplace app-eselect/eselect-repository
sudo eselect repository enable src_prepare-overlay
sudo emaint sync -r src_prepare-overlay
```

Install it using

```sh
sudo emerge -anv --autounmask net-misc/downloader-cli
```

### Manual

If you want to manuall install, clone the repo and run the following command

```sh
sudo python setup.py install
```

# Requirements

**downloader-cli** requires just one external module.

- [urllib3](https://pypi.org/project/urllib3/)

# Usage

The script also allows some other values from the commandline.

```console
usage: dw [-h] [-f | -c] [-e] [-q] [-b] [-v] SOURCE [TARGET]

positional arguments:
  SOURCE           URL of the file
  TARGET           target filepath (existing directories will be treated as
                   the target location)

optional arguments:
  -h, --help       show this help message and exit
  -f, -o, --force  overwrite if the file already exists
  -c, --resume     resume failed or cancelled download (partial sanity check)
  -e, --echo       print the filepath to stdout after downloading (other
                   output will be redirected to stderr)
  -q, --quiet      suppress filesize and progress info
  -b, --batch      Download files in batch. If this flag is passed the passed
                   source will be considered as a file with download links
                   seperated by a newline. This flag will be ignored if source
                   is a valid URL.
  -v, --version    show the program version number and exit

```

# Use It

**Want to use it in your project?**

Import the ```Download``` class using the following.

```python
from downloader_cli.download import Download
Download(url).download()
```

Above is the simplest way to use it in your app. The other arguments are optional.

## Arguments

The module takes various arguments. Only **one** is required though.

| Name | required | default |
|------|----------|---------|
| URL/file  | Yes      |         |
| des  | No       | None (Current directory is selected and the name is extracted from the URL)|
| overwrite| No   | False   |
| continue_download| No | False |
| echo | No | False |
| quiet | No | False |
| batch | No | False |
| icon_done| No   | ▓       |
| icon_left| No   | ░       |
| icon_border| No | \| (If a single char is passed, it will be used for both the right and left border. If a string of 2 chars are passed, 1st char will be used as left border and the 2nd as the right border) |

> **NOTE** For details regarding the arguments, check [Usage](#usage)

> **NOTE** In case the file size is not available, the bar is shown as indefinite, in which case the icon_left
by default space(```" "```).

# Other examples

### In case you want to experiment with the progress bar's icons, here's some examples.

- This is when I passed ```icon_done``` as ```#``` and ```icon_left``` as space.

  <div align="center" style="padding-top: 2em !important; padding-bottom: 2em; !important">
      <img src=".github/dw_other.gif">
  </div>

- In case a file's size is not available from the server, the progressbar is indefinite.

  <div align="center">
      <img src=".github/indefinite_bar.gif">
  </div>
