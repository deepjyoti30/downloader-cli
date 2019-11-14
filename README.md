<h1 align="center">downloader-cli</h1>
<h3 align="center">A simple downloader written in Python with an awesome progressbar.</h3>

<div align="center" style="padding-top: 2em !important; padding-bottom: 2em; !important">
    <img src=".github/dw.gif">
</div>

<div align="center">
<br/>

<a href="#installation">Installation</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#requirements">Requirements</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#usage">Usage</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#use-it">Use It</a>&nbsp;&nbsp;&nbsp;
<br/><br/>

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)<br/><br/>
[![License](https://img.shields.io/badge/License-MIT-pink.svg?style=for-the-badge)](LICENSE) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-purple.svg?style=for-the-badge)](http://makeapullrequest.com)

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

# Requirements

**downloader-cli** requires just one external module.

- [urllib3](https://pypi.org/project/urllib3/)

# Usage

The script also allows some other values from the commandline.

```console
usage: dw [-h] [-o] URL [des]

positional arguments:
  URL         URL of the file
  des         The name of the file to be saved with.

optional arguments:
  -h, --help  show this help message and exit
  -o          Overwrite if the file already exists else, try to resume
              download.

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

The module takes 5 arguments.

| Name | required | default |
|------|----------|---------|
| URL  | Yes      |         |
| des  | No       | None (Current directory is selected and the name is extracted from the URL)|
| overwrite| No   | False   |
| icon_done| No   | ▓       |
| icon_left| No   | ░       |

### In case you want to experiment with the progress bar's icons, here's an example.

This is when I passed ```icon_done``` as ```#``` and ```icon_left``` as space.

<div align="center" style="padding-top: 2em !important; padding-bottom: 2em; !important">
    <img src=".github/dw_other.gif">
</div>