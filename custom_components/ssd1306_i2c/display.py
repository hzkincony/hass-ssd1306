from __future__ import annotations

from dataclasses import dataclass

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

from .const import MODELS


@dataclass
class Ssd1306Display:
    i2c_bus: int
    address: int
    model: str
    rotate: int

    def _create_device(self):
        width, height = MODELS.get(self.model, MODELS["128x64"])
        serial = i2c(port=self.i2c_bus, address=self.address)
        return ssd1306(serial, width=width, height=height, rotate=self.rotate)

    def print_text(self, x: int, y: int, text: str, clear: bool = True, font_size: int = 10) -> None:
        device = self._create_device()
        if clear:
            device.clear()
        
        # Use grayscale mode for better font rendering, then convert to 1-bit
        width, height = MODELS.get(self.model, MODELS["128x64"])
        image = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(image)
        
        # Try to load a TrueType font for better rendering quality
        font = None
        # Common font paths on Linux/Raspberry Pi
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except (OSError, IOError):
                continue
        
        # Fallback to default font if no TrueType font found
        if font is None:
            try:
                font = ImageFont.load_default(size=font_size)
            except TypeError:
                font = ImageFont.load_default()
        
        safe_text = text.encode("ascii", errors="ignore").decode("ascii")
        draw.text((x, y), safe_text, font=font, fill=255, anchor="lt")
        
        # Convert to 1-bit using lower threshold to preserve all strokes
        # Lower threshold ensures thin strokes (like middle bar of 'E') are visible
        image = image.point(lambda p: 255 if p > 64 else 0, mode="1")
        
        # Display the image
        device.display(image)
