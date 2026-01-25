from __future__ import annotations

import logging
from dataclasses import dataclass

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw

from .const import MODELS
from .font8x8 import FONT8X8_BASIC_TR

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

        # Render directly to 1-bit for crisp bitmap output
        width, height = MODELS.get(self.model, MODELS["128x64"])
        image = Image.new("1", (width, height), 0)
        draw = ImageDraw.Draw(image)
        safe_text = text.encode("ascii", errors="ignore").decode("ascii")

        char_width = 8
        char_height = 8
        cx = x
        for ch in safe_text:
            code = ord(ch)
            if 0 <= code < len(FONT8X8_BASIC_TR):
                glyph = FONT8X8_BASIC_TR[code]
            else:
                glyph = FONT8X8_BASIC_TR[0]

            for col, col_bits in enumerate(glyph):
                for row in range(char_height):
                    if col_bits & (1 << row):
                        draw.point((cx + col, y + row), fill=1)

            cx += char_width

        # Display the image
        device.display(image)
