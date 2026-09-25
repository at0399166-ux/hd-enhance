from PIL import Image, ImageFilter, ImageEnhance
from pathlib import Path

def enhance_image(src: Path, out: Path, scale: int, sharpen: float, denoise: int):
    img = Image.open(src).convert("RGB")
    if denoise:
        # Gentle denoise; keeps the image natural on phones.
        img = img.filter(ImageFilter.MedianFilter(size=3))
    w, h = img.size
    img = img.resize((w * scale, h * scale), Image.Resampling.LANCZOS)
    if sharpen > 0:
        img = ImageEnhance.Sharpness(img).enhance(1.0 + min(sharpen, 3.0))
    img.save(out, "JPEG", quality=95, optimize=True)
