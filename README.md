# img2txt

Turn an image into text using unicode braille symbols. Includes color support for 4-bit ANSI, 8-bit ANSI, True Color ANSI, and HTML.

## Getting Started

### Prerequisites

- Python >= 3.10
- Pillow >= 8.4.0

### Installation

Clone the project into your local file system and run `pip install .`. It is recommended you do this in a virtual environment.

### Running

After installation, the program may be run directly by using `img2txt`, or through the module using `python3 -m img2txt`.

Usage:
```
usage: img2txt [-h] [--method {luminance,lightness}] [--tolerance TOLERANCE]
               [--invert]
               [--color {none,4bitansi,8bitansi,truecoloransi,html}]
               [--limit LIMIT] [--output OUTPUT]
               image

Convert image to text.

positional arguments:
  image

options:
  -h, --help            show this help message and exit
  --method {luminance,lightness}, -m {luminance,lightness}
                        Select method to use to determine if a pixel should be
                        included in the image.
  --tolerance TOLERANCE, -t TOLERANCE
                        Tolerance limit for determinance method.
  --invert, -i          Include this flag to invert the determinance method.
  --color {none,4bitansi,8bitansi,truecoloransi,html}, -c {none,4bitansi,8bitansi,truecoloransi,html}
                        Select color display method.
  --limit LIMIT, -l LIMIT
                        Enforce character limit.
  --output OUTPUT, -o OUTPUT
                        Output file.

```

## Authors

- Willow Ciesialka

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE VERSION 3. See [LICENSE](LICENSE) for details.
