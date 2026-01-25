from __future__ import annotations

import logging
from dataclasses import dataclass, field

from luma.core.interface.serial import i2c
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
    _device: ssd1306 | None = field(default=None, init=False, repr=False)
    _image: Image.Image | None = field(default=None, init=False, repr=False)
    _draw: ImageDraw.ImageDraw | None = field(default=None, init=False, repr=False)

    def _ensure_device(self) -> ssd1306:
        if self._device is None:
            width, height = MODELS.get(self.model, MODELS["128x64"])
            serial = i2c(port=self.i2c_bus, address=self.address)
            self._device = ssd1306(serial, width=width, height=height, rotate=self.rotate)
        return self._device

    def _ensure_buffer(self, width: int, height: int) -> None:
        if self._image is None or self._image.size != (width, height):
            self._image = Image.new("1", (width, height), 0)
            self._draw = ImageDraw.Draw(self._image)

    def print_text(self, x: int, y: int, text: str, clear: bool = True, font_size: int = 10) -> None:
        device = self._ensure_device()
        if clear:
            device.clear()

        width, height = device.size
        self._ensure_buffer(width, height)
        if self._image is None or self._draw is None:
            return
        if clear:
            self._draw.rectangle((0, 0, width, height), fill=0)
        safe_text = text.encode("ascii", errors="ignore").decode("ascii")

        try:
            font = ImageFont.load_default(size=font_size)
        except TypeError:
            font = ImageFont.load_default()
        self._draw.text((x, y), safe_text, fill=1, font=font)

        # Display the image
        device.display(self._image)
