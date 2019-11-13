<h1 align="center">downloader-cli</h1>
<h3 align="center">A simple downloader written in Python with an awesome progressbar.</h3>

<div align="center" style="padding-top: 2em !important; padding-bottom: 2em; !important">
    <img src=".github/dw.gif">
</div>

> I know the GIF says 'dw', but you need to use 'dl'

<div align="center">
<br/>

<a href="#installation">Installation</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#requirements">Requirements</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#usage">Usage</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#use-it">Use It</a>&nbsp;&nbsp;&nbsp;
<br/><br/>

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)<br/><br/>
[![License](https://img.shields.io/badge/License-MIT-pink.svg?style=for-the-badge)](LICENSE) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-purple.svg?style=for-the-badge)](http://makeapullrequest.com)

</div>

# Installation

Just clone the repo and alias the ```download.py``` to something like ```dw``` and you're good to go.

```sh
git clone https://github.com/deepjyoti30/downloader-cli
```

# Requirements

Make sure that you have the following python modules installed.

- [urllib3](https://pypi.org/project/urllib3/)

> Use the ```requirements.txt``` file to install them.

```sh
pip install -r requirements.txt
```

> Run the command with ```sudo``` if you get permission denied.

# Usage

The script also allows some other values from the commandline.

```console
usage: dl [-h] [-o] URL [des]

positional arguments:
  URL         URL of the file
  des         The name of the file to be saved with.

optional arguments:
  -h, --help  show this help message and exit
  -o          Overwrite if the file already exists else, try to resume
              download.

```

# Permanent installation
Just run these commands while in the cloned directory.
```chmod +x dl```
```sudo cp dl /usr/bin/dl```

# Use It

**Want to use it in your project?**

Just include the file in your project directory and import it. It's simple to use it.

```python
from download import Download
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

> I know the GIF says 'dw', but you need to use 'dl'
