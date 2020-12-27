#!/usr/bin/env python3

from os import environ
from random import choice, randrange
from signal import pause
from sys import stdout
from time import sleep

from colorzero import Color, Hue
from gpiozero import LEDBoard
from gpiozero.tools import random_values, scaled
from tree import RGBXmasTree


def red(delay: float = 1.0) -> None:
    """Run a simple scenario for the V1 (red LED's) tree."""
    ports = [2] + list(range(4, 28))
    tree = LEDBoard(*ports, pwm=True)
    for led in tree:
        if led.pin.number == 2:
            led.on()
        else:
            led.source_delay = delay
            led.source = scaled(random_values(), 0, 0.5)
    pause()


def rgb_rainbow(delay: float = None) -> None:
    """Run a simple scenario for the V2 (RGB LED's) tree.

    This sample is a moving rainbow. Parameters are:
        divider: number of rainbow sequences on the tree
        delta_led (calculated): hue delta between LED's
        delta_loop: hue delta between loops (how fast are we moving)

    These LED's are very bright, we reduce brightness at tree level and also
    in the initial color definition.

    More examples available at: https://github.com/ThePiHut/rgbxmastree
    """
    tree = RGBXmasTree(brightness=0.1)
    color = Color(0.1, 0, 0)
    divider = 4
    delta_led = Hue(deg=360 / 25 * divider)
    delta_loop = Hue(deg=20)
    state = [color + Hue(delta_led * i) for i in range(25)]
    try:
        while True:
            tree.value = state
            state = [s + delta_loop for s in state]
            if delay:
                sleep(delay)
    except Exception as e:
        print(e)
        tree.color = (0, 0, 0)
        tree.close()


def rgb_cycle(delay: float = 1.0) -> None:
    """Cycle trough a list of colors.

    Code from https://github.com/ThePiHut/rgbxmastree
    """
    tree = RGBXmasTree(brightness=0.1)
    colors = [Color('red'), Color('green'), Color('blue')]
    try:
        while True:
            for color in colors:
                tree.color = color
                if delay:
                    sleep(delay)
    except Exception as e:
        print(e)
        tree.color = (0, 0, 0)
        tree.close()


def rgb_random(delay: float = None) -> None:
    """Random sparkles (full)."""
    tree = RGBXmasTree(brightness=0.1)
    color = Color(0.1, 0, 0)
    try:
        while True:
            pixel = choice(tree)
            pixel.color = color + Hue(deg=randrange(360))
            if delay:
                sleep(delay)
    except Exception as e:
        print(e)
        tree.color = (0, 0, 0)
        tree.close()


def rgb_random_half(delay: float = None) -> None:
    """Random sparkles (half).

    Approximately half of the LED's will be on
    """
    tree = RGBXmasTree(brightness=0.1)
    color = Color(0.1, 0, 0)
    try:
        while True:
            pixel = choice(tree)
            if pixel.value == (0, 0, 0):
                pixel.color = color + Hue(deg=randrange(360))
            else:
                pixel.off()
            if delay:
                sleep(delay)
    except Exception as e:
        print(e)
        tree.color = (0, 0, 0)
        tree.close()


# Define additional scenarios hereunder and add them to the tree_map
# You can then select the scenario by changing the XMAS_TREE_TYPE variable.

# Map XMAS_TREE_TYPE to scenarios
tree_map = {
    'red': red,
    'rgb': rgb_rainbow,
    'rgb-rainbow': rgb_rainbow,
    'rgb-cycle': rgb_cycle,
    'rgb-random': rgb_random,
    'rgb-random-half': rgb_random_half,
}

if __name__ == '__main__':
    if environ.get('BALENA'):
        # Expunge unexpanded variables from docker-compose
        for key, val in environ.items():
            if key.startswith('XMAS_') and val.startswith('${'):
                environ.pop(key)

    tree_type = environ.get('XMAS_TREE_TYPE')
    delay = environ.get('XMAS_DELAY')
    if not tree_type:
        print('XMAS_TREE_TYPE must be defined')
    elif tree_type in tree_map:
        if delay:
            try:
                delay = float(delay)
            except ValueError:
                print(f'Cannot convert delay ({delay}) to float, reverting to default')
                delay = None
        print(f'Running {tree_type} scenario - delay: {delay}')
        stdout.flush()
        args = [] if delay is None else [delay]
        tree_map[tree_type](*args)
    else:
        print(f'Unknown XMAS_TREE_TYPE: {tree_type}')
    print('Terminating')

    # Do not respawn immediately if we are running in a container
    if environ.get('IS_CONTAINER'):
        stdout.flush()
        sleep(60)
