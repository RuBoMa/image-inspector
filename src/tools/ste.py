import numpy as np
from PIL import Image


def extract_lsb_variants(image_path, bit_position=0):
    """
    Extracts LSB data from different RGB channel variants.
    bit_position=0 -> least significant bit
    """

    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)

    # DRY: define channel selectors
    channels = {
        "interleaved": arr.reshape(-1),
        "red_only": arr[:, :, 0].reshape(-1),
        "green_only": arr[:, :, 1].reshape(-1),
        "blue_only": arr[:, :, 2].reshape(-1),
    }

    results = {}

    for name, pixels in channels.items():
        bits = (pixels >> bit_position) & 1
        results[name] = np.packbits(bits).tobytes()

    return results