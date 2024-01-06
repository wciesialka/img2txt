import argparse
from img2txt.methods import THRESHOLD_METHODS, COLOR_METHODS
from img2txt.characters.coloredtext import ColoredText

def main():
    argparser = argparse.ArgumentParser(description="Convert image to text.")
    argparser.add_argument("--method", action="store", choices=THRESHOLD_METHODS.keys())
    argparser.add_argument("--invert", action='store_true', help="Invert determinance method.")
    argparser.add_argument("--color", action="store", choices=COLOR_METHODS.keys(), default="none")
    argparser.add_argument("image", action="store", type=argparse.FileType("rb"))

    


if __name__ == "__main__":
    main()