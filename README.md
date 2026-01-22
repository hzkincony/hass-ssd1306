# SSD1306 I2C Display for Home Assistant

A minimal Home Assistant custom integration for SSD1306 I2C displays. This integration allows you to display ASCII text on OLED screens connected via I2C.

## Prerequisites

This integration requires the following Python dependencies:
- `luma.oled>=3.13.0`
- `Pillow>=9.0.0`
- `smbus2>=0.4.3`

## Installation

1. Copy the `custom_components/ssd1306_i2c` directory into your Home Assistant `custom_components` folder.
2. Restart Home Assistant.

## Configuration

Add the integration to your `configuration.yaml`. This integration supports multiple displays by providing a list of configurations.

```yaml
ssd1306_i2c:
  - model: "SSD1306 128x64"
    address: 0x3C
    i2c_bus: 1
    rotate: 0
```

### Configuration Variables

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `model` | string | `SSD1306 128x64` | Display model. Supported: `SSD1306 128x64`, `SSD1306 128x32`. |
| `address` | integer | `0x3C` | I2C address of the display (e.g., `0x3C` or `60`). |
| `i2c_bus` | integer | `1` | I2C bus number. |
| `rotate` | integer | `0` | Rotation of the display. Supported values: `0`, `1`, `2`, `3`. |
| `reset_pin` | integer | (Optional) | Ignored. Currently not supported by the integration. |

## Services

### `ssd1306_i2c.print_text`

Prints ASCII text to the configured display(s).

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `x` | integer | Yes | X coordinate in pixels (0-127). |
| `y` | integer | Yes | Y coordinate in pixels (0-63). |
| `text` | string | Yes | Text to render. |
| `clear` | boolean | No | Clear the display before printing. Default: `true`. |

#### Service Call Example

```yaml
service: ssd1306_i2c.print_text
data:
  x: 0
  y: 0
  text: "Hello World"
  clear: true
```

## Limitations

- ASCII only: non-ASCII characters are stripped before rendering.
- `reset_pin` is accepted but ignored by the integration.
- YAML-only configuration (no config flow).
