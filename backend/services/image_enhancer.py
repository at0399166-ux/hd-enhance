from PIL import Image, ImageFilter, ImageEnhance
from pathlib import Path


def enhance_image(src: Path, out: Path, scale: int, sharpen: float, denoise: int):
    # Open image
    img = Image.open(src).convert("RGB")

    # Light noise reduction
    if denoise:
        img = img.filter(ImageFilter.MedianFilter(size=3))

    # Upscale with high-quality Lanczos
    w, h = img.size
    new_size = (w * scale, h * scale)
    img = img.resize(new_size, Image.Resampling.LANCZOS)

    # Improve contrast slightly
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(1.08)

    # Improve color slightly
    color = ImageEnhance.Color(img)
    img = color.enhance(1.05)

    # Stronger sharpening
    if sharpen > 0:
        img = ImageEnhance.Sharpness(img).enhance(
            1.0 + min(float(sharpen), 4.0)
        )

        # Extra edge enhancement
        img = img.filter(ImageFilter.UnsharpMask(
            radius=1.5,
            percent=140,
            threshold=3
        ))

    # Save high-quality JPEG
    img.save(
        out,
        "JPEG",
        quality=98,
        subsampling=0,
        optimize=True
    )
