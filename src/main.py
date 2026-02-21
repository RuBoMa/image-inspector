import argparse
import os

from tools.metadata import format_exif, get_exif_data, get_gps_data
from utils.pdf import save_as_pdf

OUTPUT_DIR = "output"

def parse_args():
    usage_examples = """
Usage Examples:
    
  Extract metadata from an image:
    python3 main.py -m image.jpg -o output_metadata
    
  Detect and extract hidden data from an image using steganography:
    python3 main.py -s image.jpg -o output_stego
    
  Generate PDF output:
    python3 main.py -m image.jpg -o output_metadata --pdf
    """
    
    parser = argparse.ArgumentParser(
        description="Welcome to Image Inspector! A powerful tool for extracting metadata and detecting hidden data in images.",
        epilog=usage_examples,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-m", "--metadata", help="Extract and display metadata from an image file")
    parser.add_argument("-s", "--steganography", help="Detect and extract hidden data from an image using steganography")
    parser.add_argument("-o", "--output", help="Output file name (without extension)")
    parser.add_argument("-p", "--pdf", action="store_true", help="Export results as PDF instead of text")

    return parser.parse_args()

def validate_image(path: str):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')
    if not path.lower().endswith(valid_extensions):
        raise ValueError(f"Unsupported file type: {path}. Supported types are: {', '.join(valid_extensions)}")
    
def handle_metadata(image_path: str):
    validate_image(image_path)

    exif = get_exif_data(image_path)
    if not exif:
        print("No EXIF metadata found.")
        return None

    gps = get_gps_data(exif)

    formatted_exif = format_exif(exif)

    lines = []
    lines.append("Metadata found:")
    lines.append(formatted_exif)

    if gps:
        lines.append("\nGPS Data:")
        for key, value in gps.items():
            lines.append(f"{key}: {value}")

    return "\n".join(lines)

def main():
    args = parse_args()
    result_text = None

    if args.metadata:
        image_path = args.metadata
        result_text = handle_metadata(image_path)

    if args.steganography:
        # Placeholder for steganography detection and extraction logic
        print("Steganography detection and extraction is not implemented yet.")
        return
    
    if args.output:
        if result_text is None:
            print("No results to save. Try extracting metadata first.")
            return
        try:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            
            # Determine file extension based on --pdf flag
            if args.pdf:
                file_path = os.path.join(OUTPUT_DIR, f"{args.output}.pdf")
                save_as_pdf(file_path, result_text)
            else:
                file_path = os.path.join(OUTPUT_DIR, f"{args.output}.txt")
                with open(file_path, "w") as f:
                    f.write(result_text)
            
            print(f"Results saved to {file_path}")
        except (IOError, OSError, PermissionError) as e:
            print(f"Error writing file: {str(e)}")
        except ImportError as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":    
    main()