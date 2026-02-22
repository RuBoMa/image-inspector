import os
from tools.metadata import handle_metadata
from utils.parser import parse_args
from tools.steganography import handle_steganography

OUTPUT_DIR = "output"

def main():
    args = parse_args()
    results = []

    if not args.metadata and not args.steganography:
        print("Error: Please specify -m and/or -s")
        return

    if args.metadata:
        metadata_output = handle_metadata(args.image)
        print(metadata_output)
        results.append(metadata_output)

    if args.steganography:
        stego_output = handle_steganography(args.image)
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