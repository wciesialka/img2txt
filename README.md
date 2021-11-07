# ascii-dotter

Turn an image into "ASCII Art" using Braille Unicode characters.

## Preamble

As I write this section of my README, it is 11/6/2021. I worked on this project initially almost four years ago, in 2018. It was the first project I was proud of. However, looking at it on my GitHub pinned now brings me a great amount of shame. I no longer like how I handled this program. I violated (albiet at the time, unknowlingly) many software engineering philosophies, and incidentally followed many design anti-patterns. I decided in a energy-drink fueled haze that I would rewrite the entire program, base-up, to the best of my current ability. After this, I hope to create something I can once again be proud of. Then again, in three years time, I might just rewrite it again.

## Getting Started

### Requirements

This project was built using Python 3.8.10. A terminal that supports unicode characters is recommended, but not required. Please see [requirements.txt](requirements.txt) for module requirements.

### Running

This is a CLI program. It can be run using `python3 main.py` or `./main.py`. The list of flags are as follows:

```
usage: main.py [-h] [--output OUTPUT] [--tolerance TOLERANCE] [--method METHOD] [--invert] input
    -h: Displays help message.
    --output, -o: Output text stream. Optional. Default is sys.stdout.
    --tolerance, -t: Float in range [0.0, 1.0]. Any pixel with a luminance value greater than or equal to this value will be plotted. Default is 0.5.
    --method, -m: Which method to use for determining the luminance value of a pixel. Luminance values are mapped to [0.0, 1.0]. Methods are as follows:
        "average", "a": Calculate luminance by taking average of r, g, b.
        "relative", "r": Calculate luminance by using the [relative luminance](https://en.wikipedia.org/wiki/Relative_luminance) formula. Default.
        "value", "v": Calculate luminance by calculating the value of the pixel in HSV space.
        "weighted", "w": Calculate luminance by summing the r, g, and b values weighted by their wavelengths.
    --invert, -i: Invert output image.
    input: Binary input stream of image. Required. 

```

 
 ## Authors
 
 - Will Ciesialka

 ## License

 This project is licensed under the GNU GENERAL PUBLIC LICENSE VERSION 3. See [LICENSE](LICENSE) for details.