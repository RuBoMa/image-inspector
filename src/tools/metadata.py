import math
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def get_exif_data(image_path):
    with Image.open(image_path) as image:
        return image.getexif()


def get_gps_data(exif_data):
    if not exif_data:
        return {}

    gps_ifd = exif_data.get_ifd(0x8825)
    if not gps_ifd:
        return {}

    gps_info = {
        GPSTAGS.get(k, k): v
        for k, v in gps_ifd.items()
    }

    def to_decimal(values):
        try:
            d, m, s = (float(v) for v in values)
            return d + (m / 60.0) + (s / 3600.0)
        except Exception:
            return None

    lat = to_decimal(gps_info.get("GPSLatitude"))
    lon = to_decimal(gps_info.get("GPSLongitude"))

    if lat is None or lon is None:
        return {}

    if gps_info.get("GPSLatitudeRef") == "S":
        lat = -lat
    if gps_info.get("GPSLongitudeRef") == "W":
        lon = -lon

    return {
        "latitude": round(lat, 6),
        "longitude": round(lon, 6)
    }


def format_exif(exif_data):
    if not exif_data:
        return "No EXIF metadata found."

    lines = ["Metadata found:\n"]

    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        lines.append(f"{tag_name}: {value}")

    return "\n".join(lines)