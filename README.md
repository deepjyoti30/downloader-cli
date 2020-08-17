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

The package is available in PyPi [here](https://pypi.org/project/downloader-cli/)

Install it using

```sh
pip install downloader-cli
```

If you want to manuall install, clone the repo and run the following command

```sh
sudo python setup.py install
```

**The packages available in PyPi and AUR contain the last release, if you want all the latest changes, clone the repo and install manually or wait for the next release.**

# Requirements

**downloader-cli** requires just one external module.

- [urllib3](https://pypi.org/project/urllib3/)

# Usage

The script also allows some other values from the commandline.

```console
usage: dw [-h] [-f | -c] [-e] [-q] [-v] SOURCE [TARGET]

positional arguments:
  SOURCE           URL of the file. Alternately a file containing URL's with
                   each URL in a new line can be passed.
  TARGET           target filepath (existing directories will be treated as
                   the target location)

optional arguments:
  -h, --help       show this help message and exit
  -f, -o, --force  overwrite if the file already exists
  -c, --resume     resume failed or cancelled download (partial sanity check)
  -e, --echo       print the filepath to stdout after downloading (other
                   output will be redirected to stderr)
  -q, --quiet      suppress filesize and progress info
  -v, --version    Show the current version

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