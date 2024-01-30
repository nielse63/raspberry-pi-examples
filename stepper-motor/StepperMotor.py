#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from enum import Enum
from threading import Thread

print("mode", GPIO.getmode())
GPIO.setmode(GPIO.BCM)
DEFAULT_MAX_STEP_COUNT = 512


class Direction(Enum):
    FORWARD = -1
    BACKWARD = 1


class StepperMotor:
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
    instances = []

    @staticmethod
    def add_instance(instance) -> None:
        StepperMotor.instances.append(instance)

    @staticmethod
    def remove_instance(instance) -> None:
        StepperMotor.instances.remove(instance)

    @staticmethod
    def all_instances_finished() -> bool:
        for instance in StepperMotor.instances:
            if instance.running:
                return False
        return True

    def __init__(self, pins=list[int], speed=0.0025) -> None:
        self.pins = pins
        self.speed = speed
        self.direction = None
        self.running = False

        # add instance to list
        StepperMotor.add_instance(self)

    def setup(self) -> None:
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def cleanup(self) -> None:
        for pin in self.pins:
            GPIO.output(pin, GPIO.LOW)
        all_instances_finished = StepperMotor.all_instances_finished()
        StepperMotor.remove_instance(self)
        if all_instances_finished:
            GPIO.cleanup()

    def __move(self, direction: int, steps: int) -> None:
        step_counter = 0
        sequence = StepperMotor.sequence
        sequence_len = len(sequence)
        number_of_steps = steps or DEFAULT_MAX_STEP_COUNT

        self.setup()
        self.running = True
        # self.__start_time = time.time()
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
        self.running = False
        self.cleanup()

    def forward(self, steps: int = DEFAULT_MAX_STEP_COUNT) -> None:
        self.direction = Direction.FORWARD.name
        self.__move(Direction.FORWARD.value, steps)

    def backward(self, steps: int = DEFAULT_MAX_STEP_COUNT) -> None:
        self.direction = Direction.BACKWARD.name
        self.__move(Direction.BACKWARD.value, steps)


if __name__ == "__main__":
    step_motor1 = StepperMotor(pins=[4, 17, 27, 22])
    step_motor2 = StepperMotor(pins=[18, 23, 24, 25])
    try:
        Thread(target=step_motor1.forward, name="t1").start()
        Thread(target=step_motor2.forward, name="t2").start()
        # step_motor2.forward()
        # step_motor1.forward()
    except KeyboardInterrupt:
        step_motor1.cleanup()
        step_motor2.cleanup()
        exit(1)
