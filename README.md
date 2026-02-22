# Image Inspector

Image Inspector is a command-line tool for extracting EXIF metadata and scanning images for embedded PGP blocks. It can output results to the terminal, a text file, or a PDF.

## Features

- Extract EXIF metadata and GPS coordinates.
- Scan raw bytes and LSB variants for PGP blocks.
- Write combined results to .txt or .pdf.

## Requirements

- Python 3.8+ (recommended 3.11+)
- pip

Dependencies are listed in [requirements.txt](requirements.txt).

## Setup

From the project root:

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

This project does not use a config file. Behavior is controlled by CLI flags.

- Output directory: `output/` (created automatically if needed)
- Output format: `.txt` by default, `.pdf` when `-p` is supplied
- Image formats: common raster formats supported by Pillow (JPEG, PNG, etc.)

## Usage

All commands require an image path. You can run metadata extraction, steganography scanning, or both.

```zsh
# Metadata only
python3 src/main.py -m images/image-example1.jpeg

# Steganography only
python3 src/main.py -s images/image-example1.jpeg

# Both
python3 src/main.py -m -s images/image-example1.jpeg
```

### Output files

Use `-o` to save output to a file in the `output/` directory. Add `-p` to save as PDF.

```zsh
python3 src/main.py -m -s images/image-example1.jpeg -o report
python3 src/main.py -m -s images/image-example1.jpeg -o report -p
```

This creates:

- `output/report.txt` (default)
- `output/report.pdf` (with `-p`)

## How the tools work

### Metadata extraction

- Uses Pillow to read EXIF tags from the image.
- Formats tags into readable text.
- If GPS data is present, converts it to decimal latitude/longitude.

### Steganography scan

- Scans raw file bytes for inline PGP blocks.
- Extracts LSB data from multiple channel variants (interleaved, red, green, blue).
- Searches those variants for PGP block markers.

This scan is conservative: it looks for clear PGP markers rather than trying to decode arbitrary hidden payloads.

## Legal and ethical usage

Only analyze images you own or have explicit permission to inspect. This tool can surface metadata that may reveal sensitive information such as location, device identifiers, or hidden content. You are responsible for complying with local laws, privacy policies, and any relevant organizational rules. Do not use this tool to access private data without permission, to bypass security controls, or to harass or surveil others.

## Notes

- If no PGP block is found, the steganography scan prints `[-] No PGP data detected.`
- PDF generation requires `reportlab` (already included in [requirements.txt](requirements.txt)).

## Project Structure

```
image-inspector/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
│
├── src/
│   ├── main.py                  # CLI entry point and orchestrator
│   │
│   ├── tools/
│   │   ├── metadata.py          # EXIF/GPS extraction
│   │   │                         # - handle_metadata(): formats all results
│   │   │                         # - get_exif_data(): extracts EXIF tags
│   │   │                         # - get_gps_data(): parses GPS IFD
│   │   │                         # - format_exif(): returns readable EXIF
│   │   │
│   │   └── steganography.py      # Steganography scanning
│   │                             # - handle_steganography(): main handler
│   │                             # - discover_pgp(): searches raw + LSB
│   │                             # - extract_lsb_variants(): per-channel LSB
│   │                             # - validate_extracted_data(): confidence scoring
│   │
│   ├── utils/
│       ├── parser.py            # Argument parsing (parse_args)
│       └── pdf.py               # PDF output generation (save_as_pdf)
│
├── images/                       # Sample images for testing
│   ├── image-example1.jpeg
│   ├── image-example2.jpeg
│   └── ...
│
└── output/                       # Generated reports (auto-created)
    ├── report.txt
    ├── report.pdf
    └── ...
```

### Key modules

- **main.py** — CLI interface; calls handlers, manages output format
- **tools/metadata.py** — EXIF/GPS parsing using Pillow
- **tools/ste.py** — LSB extraction and PGP pattern scanning
- **utils/parser.py** — Argument parsing with argparse
- **utils/pdf.py** — PDF rendering with reportlab