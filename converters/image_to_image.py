from PIL import Image
from pathlib import Path


def image_to_image(input_path: str, output_format: str) -> str:
    img = Image.open(input_path)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_ext = output_format.lower()
    output_path = output_dir / f"{Path(input_path).stem}.{output_ext}"

    if output_format.upper() == "JPEG":
        img = img.convert("RGB")

    img.save(output_path, output_format.upper())
    return str(output_path)
