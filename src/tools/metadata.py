import math
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def get_exif_data(image_path: str) -> dict:
    """Extract EXIF data as readable tag names."""
    with Image.open(image_path) as image:
        return image.getexif()



def convert_to_degrees(values):
    """Convert GPS (degrees, minutes, seconds) to decimal."""
    try:
        d, m, s = (float(v) for v in values)

        if any(math.isnan(x) for x in (d, m, s)):
            return None

        return d + (m / 60.0) + (s / 3600.0)

    except (TypeError, ValueError, ZeroDivisionError):
        return None


def get_gps_data(exif_data: dict) -> dict:
    if not exif_data:
        return {}
    
    # 34853 = GPSInfo tag
    gps_ifd = exif_data.get_ifd(0x8825)
    print("RAW GPS IFD:", gps_ifd)
    if not gps_ifd:
        return {}

    gps_data = {
        GPSTAGS.get(key, key): value
        for key, value in gps_ifd.items()
    }

    lat_values = gps_data.get("GPSLatitude")
    lon_values = gps_data.get("GPSLongitude")

    if not lat_values or not lon_values:
        return {}

    lat = convert_to_degrees(lat_values)
    lon = convert_to_degrees(lon_values)

    if lat is None or lon is None:
        return {}

    # Apply hemisphere
    if gps_data.get("GPSLatitudeRef") == "S":
        lat = -lat
    if gps_data.get("GPSLongitudeRef") == "W":
        lon = -lon

    return {
        "latitude": round(lat, 6),
        "longitude": round(lon, 6),
    }

def format_exif(exif_data: dict) -> dict:
    formatted = []
    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        formatted.append(f"{tag_name}: {value}")
    return "\n".join(formatted)