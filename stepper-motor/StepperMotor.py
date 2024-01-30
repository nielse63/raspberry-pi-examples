#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from enum import Enum

DEFAULT_MAX_STEP_COUNT = 512


class Direction(Enum):
    FORWARD = -1
    BACKWARD = 1


class StepperMotor:
    # max_step_count = 512
    sequence = [
        [1, 0, 0, 1],
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
    ]

    def __init__(self, pins=list[int], speed=0.0025) -> None:
        self.pins = pins
        self.speed = speed
        self.direction = None
        self.running = False

        # private
        self.__start_time = None

    def setup(self) -> None:
        self.__start_time = time.time()
        print("start", time.time())
        GPIO.setmode(GPIO.BOARD)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        self.running = True

    def cleanup(self) -> None:
        diff = time.time() - self.__start_time
        print("diff", diff)
        for pin in self.pins:
            GPIO.output(pin, GPIO.LOW)
        GPIO.cleanup()
        self.running = False

    def __move(self, direction: int, steps: int) -> None:
        step_counter = 0
        sequence = StepperMotor.sequence
        sequence_len = len(sequence)
        number_of_steps = steps or DEFAULT_MAX_STEP_COUNT

        self.setup()
        for i in range(0, number_of_steps):
            for halfstep in range(0, sequence_len):
                for pin in range(0, len(self.pins)):
                    GPIO.output(self.pins[pin], sequence[step_counter][pin])
                step_counter += direction
                if step_counter >= sequence_len:
                    step_counter = 0
                if step_counter < 0:
                    step_counter = sequence_len + direction
                time.sleep(self.speed)
        self.cleanup()

    def forward(self, steps: int = DEFAULT_MAX_STEP_COUNT) -> None:
        self.direction = Direction.FORWARD.name
        self.__move(Direction.FORWARD.value, steps)

    def backward(self, steps: int = DEFAULT_MAX_STEP_COUNT) -> None:
        self.direction = Direction.BACKWARD.name
        self.__move(Direction.BACKWARD.value, steps)


if __name__ == "__main__":
    step_motor = StepperMotor(pins=[7, 11, 13, 15])
    try:
        step_motor.forward()
        step_motor.backward()
    except KeyboardInterrupt:
        step_motor.cleanup()
        exit(1)
