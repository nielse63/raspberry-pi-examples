# raspberry-pi-examples

> Examples of sensors, servers, and scripts to run on Raspberry Pi

- [Setting Up Raspberry Pi](#setting-up-raspberry-pi)
- [Development](#development)
  - [Creating a new example](#creating-a-new-example)
- [GPIO Pin Reference](#gpio-pin-reference)

## Setting Up Raspberry Pi

Install kernal dependencies:

```bash
sudo apt-get update -y
sudo apt-get updgrade -y
```

Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Or just run the setup script in this project:

```bash
.bin/setup
```

## Development

Run the dev setup script:

```bash
.bin/setup-dev
```

This will create a virtual environment, install all dependencies and a add pre-commit git hook.

### Creating a new example

```bash
node .bin/generate.js
```

## GPIO Pin Reference

![GPIO Pins](./assets/gpio-pins.png)
