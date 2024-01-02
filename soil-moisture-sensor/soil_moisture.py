#!/usr/bin/env python3
from gpiozero import MCP3008

def get_soil_moisture():
    results = MCP3008(
        channel=0,
        max_voltage=5.0,
    )
    value = results.value
    print("soil moisture: %0.3f", value)
    return value

if __name__ == '__main__':
    get_soil_moisture()
