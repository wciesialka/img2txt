#!/bin/env python3
'''Setup script.'''
from pathlib import Path
from setuptools import setup, find_packages

THIS_DIRECTORY = Path(__file__).parent

REQUIREMENTS = (THIS_DIRECTORY / "requirements.txt").read_text().split('\n')[:-1]
LONG_DESCRIPTION = (THIS_DIRECTORY / "README.md").read_text()

CONTENT = {
    "name": "AsciiDotter",
    "version": "2.1.0",
    "author": "Willow Ciesialka",
    "author_email": "wciesialka@gmail.com",
    "url": "https://github.com/wciesialka/ascii-dotter",
    "description": "CLI tool for turning images into ascii art.",
    "long_description": LONG_DESCRIPTION,
    "long_description_content_type": "text/markdown",
    "license": "GPL-3.0",
    "packages": find_packages(where="src"),
    "entry_points": {
        'console_scripts': [
            'asciidotter = ascii_dotter.__main__:cli_entry_point'
        ]
    },
    "classifiers": [
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Topic :: Artistic Software",
        "Operating System :: OS Independent"
    ],
    "keywords": "python image ascii art",
    "package_dir": {"": "src"},
    "install_requires": REQUIREMENTS,
    "zip_safe": False,
    "python_requires": ">=3.8.10"
}

setup(**CONTENT)
