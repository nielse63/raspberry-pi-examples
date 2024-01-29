#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

step_count = 4096
control_pins = [7, 11, 13, 15]
halfstep_seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
]


def setup():
    GPIO.setmode(GPIO.BOARD)
    for pin in control_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)


def cleanup():
    for pin in control_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()


def main():
    setup()

    for i in range(0, step_count):
        for halfstep in range(0, len(halfstep_seq)):
            for pin in range(0, len(control_pins)):
                GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
            time.sleep(0.002)
    cleanup()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cleanup()
        exit(1)
