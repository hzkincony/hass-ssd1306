# AGENTS.md

This repository is a minimal Home Assistant custom component for an SSD1306 I2C
display. It has no explicit build, lint, or test tooling configured. Use this
guide to keep changes consistent with existing patterns.

## Repository layout
- `custom_components/ssd1306_i2c/__init__.py`: integration setup, service
  registration, config schema (voluptuous), async setup.
- `custom_components/ssd1306_i2c/const.py`: constants, config keys, defaults.
- `custom_components/ssd1306_i2c/display.py`: device wrapper and rendering.
- `custom_components/ssd1306_i2c/display_setup.py`: helper for manual setup.
- `custom_components/ssd1306_i2c/manifest.json`: integration metadata and
  runtime dependencies.
- `custom_components/ssd1306_i2c/services.yaml`: service descriptions.
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

### Typing
- Type hints are used for function signatures and dataclasses.
- `from __future__ import annotations` is present in `display.py` only; follow
  the existing file pattern rather than forcing it everywhere.
- Use `Optional[...]` for nullable values (see `display.py`).

### Naming conventions
- Classes: `CamelCase` (e.g., `Ssd1306Display`).
- Functions/variables: `snake_case` (e.g., `handle_print_text`).
- Constants: `UPPER_SNAKE_CASE` in `const.py`.
- Private helpers: prefix with `_` (e.g., `_create_device`).

### Logging
- Standard pattern: `_LOGGER = logging.getLogger(__name__)`.
- Log warnings for unsupported config values (see reset_pin handling).

### Error handling
- No explicit try/except blocks currently; errors are allowed to bubble up.
- Prefer validating inputs with `voluptuous` schemas where possible.

### Configuration and schemas
- Configuration uses `voluptuous` schemas in `__init__.py`.
- The integration uses a list of display configs under the domain key.
- Defaults are defined in `const.py` and referenced in schemas.

### Home Assistant patterns
- `async_setup` is the primary entry point.
- Store runtime state in `hass.data[DOMAIN]`.
- Register services with `hass.services.async_register`.
- For blocking I/O, offload to executor with
  `hass.async_add_executor_job`.

### Services
- Services are defined in `services.yaml` and should match handler schema.
- `print_text` expects `x`, `y`, `text`, and optional `clear`.
- Text is sanitized to ASCII before rendering.

### Device handling
- Device creation happens per call via `_create_device` in `display.py`.
- Default model falls back to `SSD1306 128x64` if unknown.

## Dependencies
- Dependencies are declared in `custom_components/ssd1306_i2c/manifest.json`.
- Current requirements:
  - `luma.oled>=3.13.0`
  - `Pillow>=9.0.0`
  - `smbus2>=0.4.3`

## Agent workflow expectations
- Do not invent build or test commands; check the repo first.
- Keep changes minimal and consistent with existing code.
- Avoid refactors during bug fixes.
- Update `services.yaml` when adding or changing services.
- Update `manifest.json` when adding Python dependencies.

## Cursor / Copilot rules
- No `.cursor/rules/`, `.cursorrules`, or `.github/copilot-instructions.md`
  files were found in this repository.
