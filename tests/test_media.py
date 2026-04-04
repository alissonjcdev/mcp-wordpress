import io
import base64
from PIL import Image

from automation_mcp.media import optimize_image, image_to_base64


def _create_test_image(path: str, width: int = 2000, height: int = 1500) -> str:
    img = Image.new("RGB", (width, height), color=(255, 0, 0))
    img.save(path, format="PNG")
    return path


def test_optimize_resizes_large_image(tmp_path):
    input_path = str(tmp_path / "large.png")
    _create_test_image(input_path, 3000, 2000)

    data, filename = optimize_image(input_path, max_width=1200, output_format="webp")
    assert filename == "large.webp"
    assert len(data) > 0

    img = Image.open(io.BytesIO(data))
    assert img.width == 1200
    assert img.height == 800


def test_optimize_keeps_small_image(tmp_path):
    input_path = str(tmp_path / "small.png")
    _create_test_image(input_path, 800, 600)

    data, filename = optimize_image(input_path, max_width=1200, output_format="webp")
    img = Image.open(io.BytesIO(data))
    assert img.width == 800


def test_optimize_jpeg_output(tmp_path):
    input_path = str(tmp_path / "test.png")
    _create_test_image(input_path)

    data, filename = optimize_image(input_path, output_format="jpeg")
    assert filename == "test.jpg"


def test_image_to_base64():
    data = b"hello world"
    b64 = image_to_base64(data)
    assert base64.b64decode(b64) == data
