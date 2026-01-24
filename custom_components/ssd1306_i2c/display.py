from __future__ import annotations

from dataclasses import dataclass

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont

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
        try:
            font = ImageFont.load_default(size=font_size)
        except TypeError:
            font = ImageFont.load_default()
        safe_text = text.encode("ascii", errors="ignore").decode("ascii")
        with canvas(device) as draw:
            draw.text((x, y), safe_text, font=font, fill=255)
