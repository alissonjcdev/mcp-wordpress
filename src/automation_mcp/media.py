import io
import base64
from pathlib import Path
from PIL import Image


def optimize_image(
    input_path: str,
    max_width: int = 1200,
    quality: int = 85,
    output_format: str = "webp",
) -> tuple[bytes, str]:
    """Optimize image and return (bytes, filename)."""
    img = Image.open(input_path)

    # Convert RGBA to RGB for JPEG/WebP
    if img.mode in ("RGBA", "P") and output_format in ("jpeg", "webp"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        background.paste(img, mask=img.split()[-1])
        img = background

    # Resize if wider than max_width
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)

    # Save to bytes
    buffer = io.BytesIO()
    save_kwargs = {"quality": quality, "optimize": True}
    if output_format == "webp":
        img.save(buffer, format="WEBP", **save_kwargs)
    elif output_format == "jpeg":
        img.save(buffer, format="JPEG", **save_kwargs)
    elif output_format == "png":
        img.save(buffer, format="PNG", optimize=True)
    else:
        img.save(buffer, format=output_format.upper())

    # Generate filename
    stem = Path(input_path).stem
    ext = "jpg" if output_format == "jpeg" else output_format
    filename = f"{stem}.{ext}"

    return buffer.getvalue(), filename


def image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("ascii")
