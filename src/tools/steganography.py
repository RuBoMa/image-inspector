import numpy as np
from PIL import Image
import re

# For simplicity, we just return the PGP blocks as text.
def handle_steganography(path):
    pgp_blocks = discover_pgp(path)

    if not pgp_blocks:
        return "[-] No PGP data detected."

    return "\n\n".join(pgp_blocks)

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

def extract_lsb_variants(image_path, bit_position=0):
    """
    Extracts LSB data from different RGB channel variants.
    bit_position=0 -> least significant bit
    """

    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)

    # Prepare channel variants so we can detect per-channel embeddings.
    channels = {
        "interleaved": arr.reshape(-1),
        "red_only": arr[:, :, 0].reshape(-1),
        "green_only": arr[:, :, 1].reshape(-1),
        "blue_only": arr[:, :, 2].reshape(-1),
    }

    results = {}

    for name, pixels in channels.items():
        # Extract the target bit and pack into bytes for scanning.
        bits = (pixels >> bit_position) & 1
        results[name] = np.packbits(bits).tobytes()

    return results