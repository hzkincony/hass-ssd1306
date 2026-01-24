# AGENTS.md

This repository is a minimal Home Assistant custom component for an SSD1306 I2C
display. It has no explicit build, lint, or test tooling configured. Use this
guide to keep changes consistent with existing patterns.

## Repository layout
- `custom_components/ssd1306_i2c/__init__.py`: integration setup, service
  registration, config schema (voluptuous), async setup, display targeting.
- `custom_components/ssd1306_i2c/const.py`: constants, config keys, defaults,
  service attributes.
- `custom_components/ssd1306_i2c/display.py`: device wrapper and rendering with
  font size support.
- `custom_components/ssd1306_i2c/display_setup.py`: helper for manual setup.
- `custom_components/ssd1306_i2c/manifest.json`: integration metadata and
  runtime dependencies.
- `custom_components/ssd1306_i2c/services.yaml`: service descriptions with
  field definitions.
- `custom_components/ssd1306_i2c/configuration.yaml`: example config.

## Build / lint / test commands
There are no build, lint, or test commands defined in this repository.

### Build
- Not configured (no Makefile, no package scripts, no CI).

### Lint / format
- Not configured (no .flake8, no ruff, no black, no pre-commit).

### Tests
- Not configured (no tests/ directory, no pytest/tox config).

### Single test execution
- Not applicable (no test runner or tests in repo).

If you add tooling, document the exact commands here and prefer commands that
work from the repo root.

## Code style guidelines (from existing code)

### Python style
- Indentation: 4 spaces.
- Strings: double quotes used consistently.
- Line length: short, readable lines; no explicit formatter config.

### Imports
- Standard library first, then third-party, then local relative imports.
- Local imports use `from .module import ...`.
- Example ordering in `custom_components/ssd1306_i2c/__init__.py`:
  - stdlib: `import logging`
  - third-party: `import voluptuous as vol`
  - Home Assistant: `from homeassistant...`
  - local: `from .const import ...`
- Group imports from same module (e.g., all `.const` imports together).

### Typing
- Type hints are used for function signatures and dataclasses.
- `from __future__ import annotations` is present in `display.py` only; follow
  the existing file pattern rather than forcing it everywhere.
- No `Optional[...]` needed when using `from __future__ import annotations`;
  use `Type | None` or simply omit for parameters with defaults.

### Naming conventions
- Classes: `CamelCase` (e.g., `Ssd1306Display`).
- Functions/variables: `snake_case` (e.g., `handle_print_text`).
- Constants: `UPPER_SNAKE_CASE` in `const.py`.
- Config keys: lowercase with underscores (e.g., `CONF_I2C_BUS = "i2c_bus"`).
- Service attributes: lowercase with underscores (e.g., `ATTR_FONT_SIZE = "font_size"`).
- Private helpers: prefix with `_` (e.g., `_create_device`).

### Logging
- Standard pattern: `_LOGGER = logging.getLogger(__name__)`.
- Use appropriate log levels: `.error()` for failures, `.warning()` for issues.
- Log display targeting errors with available display names for debugging.

### Error handling
- Minimal try/except blocks; use them for expected failures (e.g., font loading).
- Prefer validating inputs with `voluptuous` schemas where possible.
- Fall back gracefully (e.g., `ImageFont.load_default()` if sized font fails).
- Log errors before returning early from service handlers.

### Configuration and schemas
- Configuration uses `voluptuous` schemas in `__init__.py`.
- The integration uses a list of display configs under the domain key.
- Each display can have an optional `name` for targeting.
- Defaults are defined in `const.py` and referenced in schemas.
- Use `vol.Optional(key, default=value)` for optional config with defaults.
- Use `vol.In([...])` for enum-like values (models, rotation).

### Home Assistant patterns
- `async_setup` is the primary entry point.
- Store runtime state in `hass.data[DOMAIN]` as a dict.
- Displays are stored by name in `hass.data[DOMAIN]["displays"]` dict.
- Auto-generate display names as `{i2c_bus}_{address}` if not provided.
- Register services with `hass.services.async_register`.
- For blocking I/O, offload to executor with
  `hass.async_add_executor_job(func, *args)`.

### Services
- Services are defined in `services.yaml` and should match handler schema.
- `print_text` expects `x`, `y`, `text`, and optional `clear`, `font_size`,
  `display_name`.
- `display_name` targets a specific display; if omitted, prints to all displays.
- Text is sanitized to ASCII before rendering.
- Service schemas use Home Assistant helpers (e.g., `cv.positive_int`,
  `cv.string`, `cv.boolean`).

### Device handling
- Device creation happens per call via `_create_device` in `display.py`.
- Default model falls back to `128x64` if unknown.
- Supported models: `128x64`, `128x32`, `96x16`, `64x48`, `64x32`.
- Font sizing uses `ImageFont.load_default(size=font_size)` (Pillow 10.1+).
- Falls back to unsized default font for older Pillow versions.

### Display targeting
- Multiple displays are supported via configuration list.
- Each display can have a `name` field for easy targeting.
- If no `name` provided, auto-generate as `{i2c_bus}_{address}`.
- Service call can specify `display_name` to target one display.
- If `display_name` not found, log error with available display names.

## Dependencies
- Dependencies are declared in `custom_components/ssd1306_i2c/manifest.json`.
- Current requirements:
  - `luma.oled>=3.13.0`
  - `Pillow>=10.1.0` (for font size support)
  - `smbus2>=0.4.3`

## Agent workflow expectations
- Do not invent build or test commands; check the repo first.
- Keep changes minimal and consistent with existing code.
- Avoid refactors during bug fixes.
- Update `services.yaml` when adding or changing services.
- Update `manifest.json` when adding Python dependencies.
- Update `README.md` when changing user-facing behavior.
- When adding config options, update both `const.py` and `CONFIG_SCHEMA`.
- When adding service parameters, update `const.py`, `SERVICE_SCHEMA`, and
  `services.yaml`.

## Cursor / Copilot rules
- No `.cursor/rules/`, `.cursorrules`, or `.github/copilot-instructions.md`
  files were found in this repository.
