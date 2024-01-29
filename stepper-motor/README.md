# 28BYJ-48 Stepper Motor

- [Products](#products)
- [Wiring](#wiring)
- [Setup](#setup)
- [Usage](#usage)

## Products

- 28BYJ-48 Stepper Motor
- ULN2003 Driver

## Wiring

| ULN2003 | BCM    | Pin |
| ------- | ------ | --- |
| In1     | GPIO4  | 7   |
| In2     | GPIO17 | 11  |
| In3     | GPIO27 | 13  |
| In4     | GPIO22 | 15  |
| +       | 5V     | 2   |
| -       | GND    | 6   |

![Soil Moisture Sensor](../assets/stepper-motor.jpg)

## Setup

Install dependencies:

```bash
python3 -m pip RPi.GPIO
```

## Usage

```bash
python3 ./stepper_motor.py
```
