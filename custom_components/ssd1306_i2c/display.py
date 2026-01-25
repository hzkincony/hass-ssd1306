from __future__ import annotations

import logging
from dataclasses import dataclass

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

from .const import MODELS

_LOGGER = logging.getLogger(__name__)


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

        width, height = MODELS.get(self.model, MODELS["128x64"])
        image = Image.new("1", (width, height), 0)
        draw = ImageDraw.Draw(image)
        safe_text = text.encode("ascii", errors="ignore").decode("ascii")

        try:
            font = ImageFont.load_default(size=font_size)
        except TypeError:
            font = ImageFont.load_default()
        draw.text((x, y), safe_text, fill=1, font=font)

        # Display the image
        device.display(image)
