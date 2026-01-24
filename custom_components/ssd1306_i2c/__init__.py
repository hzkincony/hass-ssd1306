import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    ATTR_CLEAR,
    ATTR_DISPLAY_NAME,
    ATTR_FONT_SIZE,
    ATTR_TEXT,
    ATTR_X,
    ATTR_Y,
    CONF_ADDRESS,
    CONF_I2C_BUS,
    CONF_MODEL,
    CONF_NAME,
    CONF_ROTATE,
    DEFAULT_ADDRESS,
    DEFAULT_FONT_SIZE,
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
                    vol.Optional(CONF_NAME): cv.string,
                    vol.Optional(CONF_MODEL, default=DEFAULT_MODEL): vol.In(
                        ["128x64", "128x32", "96x16", "64x48", "64x32"]
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
        vol.Optional(ATTR_FONT_SIZE, default=DEFAULT_FONT_SIZE): cv.positive_int,
        vol.Optional(ATTR_DISPLAY_NAME): cv.string,
    }
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    if DOMAIN not in config:
        return True

    display_configs = config.get(DOMAIN, [])

    display_entries = {}
    for idx, display_config in enumerate(display_configs):
        display = Ssd1306Display(
            i2c_bus=display_config[CONF_I2C_BUS],
            address=display_config[CONF_ADDRESS],
            model=display_config[CONF_MODEL],
            rotate=display_config[CONF_ROTATE],
        )
        name = display_config.get(CONF_NAME)
        if name:
            display_entries[name] = display
        else:
            display_entries[f"{display_config[CONF_I2C_BUS]}_{display_config[CONF_ADDRESS]}"] = display

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
        font_size = call.data[ATTR_FONT_SIZE]
        display_name = call.data.get(ATTR_DISPLAY_NAME)
        
        displays = hass.data[DOMAIN]["displays"]
        
        if display_name:
            if display_name not in displays:
                _LOGGER.error("Display '%s' not found. Available displays: %s", display_name, list(displays.keys()))
                return
            target_displays = {display_name: displays[display_name]}
        else:
            target_displays = displays
        
        for name, display in target_displays.items():
            await hass.async_add_executor_job(display.print_text, x, y, text, clear, font_size)

    hass.services.async_register(
        DOMAIN,
        SERVICE_PRINT_TEXT,
        handle_print_text,
        schema=SERVICE_SCHEMA,
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return True
