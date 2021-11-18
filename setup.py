#!/bin/env python3

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent

requirements = (this_directory / "requirements.txt").read_text().split('\n')[:-1]
long_description = (this_directory / "README.md").read_text()

content = {
    "name": "AsciiDotter",
    "version": "2.1.0",
    "author": "Willow Ciesialka",
    "author_email": "wciesialka@gmail.com",
    "url": "https://github.com/wciesialka/ascii-dotter",
    "description": "CLI tool for turning images into ascii art.",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "license": "GPL-3.0",
    "packages": find_packages(where="src"),
    "entry_points": {
        'console_scripts': [
            'asciidotter = ascii_dotter.__main__:cli_entry_point'
        ]
    },
    "classifiers": [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU Affero General Public License v3",
            "Topic :: Artistic Software",
            "Operating System :: OS Independent"
    ],
    "keywords": "python image ascii art",
    "package_dir": {"": "src"},
    "install_requires": requirements,
    "zip_safe": False,
    "python_requires": ">=3.8.10"
}

setup(**content)