import argparse
from img2txt.methods import METHODS

def main():
    argparser = argparse.ArgumentParser(description="Convert image to text.")
    argparser.add_argument("--method", action="store", choices=methods.keys())
    argparser.add_argument("--invert", action='store_true', help="Invert determinance method.")

if __name__ == "__main__":
    main()