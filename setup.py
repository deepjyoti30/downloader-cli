#!/usr/bin/env python3
"""Setup downloader-cli"""

import io
from setuptools import setup

with io.open("README.md", encoding='utf-8') as fh:
    long_description = fh.read()

requirements = [
    'urllib3>=1.25.6'
]

exec(open("downloader_cli/__version__.py").read())


setup(
    name="downloader_cli",
    version=__version__,
    author="Deepjyoti Barman",
    author_email="deep.barman30@gmail.com",
    description="A simple downloader written in Python with an awesome progressbar.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deepjyoti30/downloader-cli",
    packages=["downloader_cli"],
    classifiers=(
        [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
    ),
    entry_points={
        'console_scripts': [
            "dw = downloader_cli.download:main"
        ]
    },
    install_requires=requirements,
)
