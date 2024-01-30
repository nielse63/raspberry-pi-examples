#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

max_step_count = 512  # 512 steps = 1 revolution
control_pins = [7, 11, 13, 15]
halfstep_seq = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
]
step_count = len(halfstep_seq)
direction = -1  # -1 = clockwise, 1 = counter-clockwise
speed_delay = 0.003


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

    step_counter = 0

    for i in range(0, max_step_count):
        for halfstep in range(0, len(halfstep_seq)):
            for pin in range(0, len(control_pins)):
                GPIO.output(control_pins[pin], halfstep_seq[step_counter][pin])
            step_counter += direction
            if step_counter >= step_count:
                step_counter = 0
            if step_counter < 0:
                step_counter = step_count + direction
            time.sleep(speed_delay)
    cleanup()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cleanup()
        exit(1)
