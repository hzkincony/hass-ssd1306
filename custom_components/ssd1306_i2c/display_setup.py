import logging

import voluptuous as vol

from homeassistant.const import CONF_ADDRESS
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_I2C_BUS,
    CONF_MODEL,
    CONF_RESET_PIN,
    CONF_ROTATE,
    DEFAULT_ADDRESS,
    DEFAULT_I2C_BUS,
    DEFAULT_MODEL,
    DEFAULT_ROTATE,
    DOMAIN,
)
from .display import Ssd1306Display

_LOGGER = logging.getLogger(__name__)

DISPLAY_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_MODEL, default=DEFAULT_MODEL): vol.In(["SSD1306 128x64", "SSD1306 128x32"]),
        vol.Optional(CONF_ADDRESS, default=DEFAULT_ADDRESS): cv.positive_int,
        vol.Optional(CONF_I2C_BUS, default=DEFAULT_I2C_BUS): cv.positive_int,
        vol.Optional(CONF_RESET_PIN): cv.positive_int,
        vol.Optional(CONF_ROTATE, default=DEFAULT_ROTATE): vol.In([0, 1, 2, 3]),
    }
)


def setup_display(hass, config):
    reset_pin = config.get(CONF_RESET_PIN)
    if reset_pin is not None:
        _LOGGER.warning("reset_pin is configured but not supported; ignoring")
    display = Ssd1306Display(
        i2c_bus=config[CONF_I2C_BUS],
        address=config[CONF_ADDRESS],
        model=config[CONF_MODEL],
        reset_pin=reset_pin,
        rotate=config[CONF_ROTATE],
    )
    hass.data.setdefault(DOMAIN, {"displays": []})
    hass.data[DOMAIN]["displays"].append(display)
