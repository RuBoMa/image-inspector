import argparse
import os
import re

from tools.metadata import get_exif_data, get_gps_data, format_exif
from tools.ste import extract_lsb_variants

OUTPUT_DIR = "output"


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


def discover_pgp(image_path):
    """Scan raw file bytes and LSB data for PGP blocks."""
    pgp_pattern = re.compile(
        b"-----BEGIN PGP.*?-----END PGP.*?-----",
        re.DOTALL
    )

    found = set()

    # Scan raw bytes for a literal PGP block in the file.
    with open(image_path, "rb") as f:
        raw_data = f.read()
        matches = pgp_pattern.findall(raw_data)
        for match in matches:
            found.add(match.decode("utf-8", errors="ignore"))

    # Scan extracted LSB variants for embedded PGP blocks.
    variants = extract_lsb_variants(image_path)
    for data in variants.values():
        matches = pgp_pattern.findall(data)
        for match in matches:
            found.add(match.decode("utf-8", errors="ignore"))

    return list(found)


def handle_metadata(path):
    exif = get_exif_data(path)
    gps = get_gps_data(exif)

    report = format_exif(exif)

    if gps:
        report += (
            f"\n\nGPS Data:\n"
            f"Latitude: {gps['latitude']}\n"
            f"Longitude: {gps['longitude']}"
        )

    return report

# For simplicity, we just return the PGP blocks as text.
def handle_steganography(path):
    pgp_blocks = discover_pgp(path)

    if not pgp_blocks:
        return "[-] No PGP data detected."

    return "\n\n".join(pgp_blocks)


def main():
    args = parse_args()
    results = []

    if not args.metadata and not args.steganography:
        print("Error: Please specify -m and/or -s")
        return

    image_path = args.image

    if args.metadata:
        metadata_output = handle_metadata(image_path)
        print(metadata_output)
        results.append(metadata_output)

    if args.steganography:
        stego_output = handle_steganography(image_path)
        print("\n" + stego_output if results else stego_output)
        results.append(stego_output)

    if args.output and results:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        combined_output = "\n\n".join(results)
        
        if args.pdf:
            try:
                from utils.pdf import save_as_pdf
                file_path = os.path.join(OUTPUT_DIR, f"{args.output}.pdf")
                save_as_pdf(file_path, combined_output)
                print(f"\nResults saved to {file_path}")
            except ImportError:
                print("Error: reportlab not installed. Install with: pip install reportlab")
            except Exception as e:
                print(f"Error creating PDF: {e}")
        else:
            file_path = os.path.join(OUTPUT_DIR, f"{args.output}.txt")
            with open(file_path, "w") as f:
                f.write(combined_output)
            print(f"\nResults saved to {file_path}")


if __name__ == "__main__":
    main()