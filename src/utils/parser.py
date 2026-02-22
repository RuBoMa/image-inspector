import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Image Inspector: Metadata and Steganography Tool."
    )
    parser.add_argument("-m", "--metadata", action="store_true", help="Extract metadata from image")
    parser.add_argument("-s", "--steganography", action="store_true", help="Enable steganography/PGP scan")
    parser.add_argument("image", help="Image path")
    parser.add_argument("-o", "--output", help="Output filename (no extension)")
    parser.add_argument("-p", "--pdf", action="store_true", help="Export results as PDF")
    
    return parser.parse_args()
