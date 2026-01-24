import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    ATTR_CLEAR,
    ATTR_TEXT,
    ATTR_X,
    ATTR_Y,
    CONF_ADDRESS,
    CONF_I2C_BUS,
    CONF_MODEL,
    CONF_ROTATE,
    DEFAULT_ADDRESS,
    DEFAULT_I2C_BUS,
    DEFAULT_MODEL,
    DEFAULT_ROTATE,
    DOMAIN,
    SERVICE_PRINT_TEXT,
)
from .display import Ssd1306Display

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            cv.ensure_list,
            [
                {
                    vol.Optional(CONF_MODEL, default=DEFAULT_MODEL): vol.In(
                        ["SSD1306 128x64", "SSD1306 128x32"]
                    ),
                    vol.Optional(CONF_ADDRESS, default=DEFAULT_ADDRESS): cv.positive_int,
                    vol.Optional(CONF_I2C_BUS, default=DEFAULT_I2C_BUS): cv.positive_int,
                    vol.Optional(CONF_ROTATE, default=DEFAULT_ROTATE): vol.In([0, 1, 2, 3]),
                }
            ],
        ),
    },
    extra=vol.ALLOW_EXTRA,
)

SERVICE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_X): cv.positive_int,
        vol.Required(ATTR_Y): cv.positive_int,
        vol.Required(ATTR_TEXT): cv.string,
        vol.Optional(ATTR_CLEAR, default=True): cv.boolean,
    }
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    if DOMAIN not in config:
        return True

    display_configs = config.get(DOMAIN, [])

    display_entries = []
    for display_config in display_configs:
        display = Ssd1306Display(
            i2c_bus=display_config[CONF_I2C_BUS],
            address=display_config[CONF_ADDRESS],
            model=display_config[CONF_MODEL],
            rotate=display_config[CONF_ROTATE],
        )
        display_entries.append(display)

    if not display_entries:
        _LOGGER.error("No '%s' displays configured", DOMAIN)
        return False

    hass.data[DOMAIN] = {
        "displays": display_entries,
    }

    async def handle_print_text(call):
        x = call.data[ATTR_X]
        y = call.data[ATTR_Y]
        text = call.data[ATTR_TEXT]
        clear = call.data[ATTR_CLEAR]
        for display in hass.data[DOMAIN]["displays"]:
            await hass.async_add_executor_job(display.print_text, x, y, text, clear)

    hass.services.async_register(
        DOMAIN,
        SERVICE_PRINT_TEXT,
        handle_print_text,
        schema=SERVICE_SCHEMA,
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return True
