#!/usr/bin/env python3
import os

ds18b20 = ""


def convert_to_f(temp):
    temp_f = temp * 1.8000 + 32
    return round(temp_f, 2)


def setup():
    global ds18b20
    for i in os.listdir("/sys/bus/w1/devices"):
        if i != "w1_bus_master1" and not ds18b20:
            ds18b20 = i


def get_temperature():
    if not ds18b20:
        setup()
    location = "/sys/bus/w1/devices/" + ds18b20 + "/w1_slave"
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    temperature = temperature / 1000
    return


def main():
    setup()
    temp_c = get_temperature()
    temp_f = convert_to_f(temp_c)
    print("Temperature: %0.3f C / %0.3f F" % (temp_c, temp_f))


if __name__ == "__main__":
    main()
