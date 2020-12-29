# XMas Tree Container

## Overview

Simple sample setup to drive the [3D Xmas Tree for Raspberry Pi](https://thepihut.com/xmas) from [The Pi Hut](https://thepihut.com/) using containers, either with [balenaCloud](https://www.balena.io/) or with [Docker](https://docs.docker.com/get-started/overview/) / [Docker Compose](https://docs.docker.com/compose/)

The code skeleton supports the original 3D Xmas Tree with red LED's as well as the latest one with addressable RGB LED's; the same container can be used on several device using the `XMAS_TREE_TYPE` environment variable to select the hardware or the LED animation _scenario_.

Included _scenarios_:

- Original tree:
  - red
  - red-random: randomly sparkle pixels
- RGB Tree:
  - rgb / rgb-rainbow: rainbow effect
  - rgb-cycle: cycle through red, green and blue, changing pixel-by-pixel
  - rgb-random: randomly sparkle all the pixels
  - rgb-random-half: randomly sparkle half of the pixels

## Adding a _scenario_

You can easily add new animation _scenarios_ by adding a function in [`xmas-tree.py`](xmas-tree/xmas-tree.py) and a new entry in the `tree_map` dictionary.

The function must accept an optional float _delay_ parameter.

## Usage

### balenaCloud

Create a new application, provision a device and push this repository with the Balena CLI. E.g:

```shell
balena push <My XMas App>
```

If you are unfamiliar with balenaCloud, follow the steps described in [Get started with Raspberry Pi](https://www.balena.io/docs/learn/getting-started/raspberry-pi/python/).

Define a Device variable or a Device Service variable for you device named `XMAS_TREE_TYPE` with the value for your animation _scenario_ (see above list).

Optionally define a `XMAS_DELAY` variable to change the speed of the animation. The meaning and default value for the delay is _scenario_ dependant.

That's it!

When you change the value of a variable, your container will be automatically restarted and the new parameters.

If you make changes to `xmas-tree.py`, run `balena push` to rebuild the container and update your devices.

### Docker / Docker Compose

If you prefer, you can use directly Docker and Docker Compose on your Pi.

Copy the [`.env-distr`](./.env-distr) file to `.env` and configure:

- `MACHINE_NAME`: your Raspberry Pi version
- `XMAS_TREE_TYPE`: the selected tree type / animation _scenario_
- `XMAS_DELAY` (optional): change the speed of the animation. The meaning and default value for the delay is _scenario_ dependant.

Build the container:

```shell
docker compose build
```

Run the container:

```shell
docker compose up
```

To change the _scenario_ or the delay, edit the `.env` file, bring you container `down` and `up` again.

Changes in `xmas-tree.py` will require a new `build`.

## License

The code in this repository contains sample code from [The Pi Hut](https://thepihut.com/) which does not specify any licence and by default is _All Rights Reserved_.
