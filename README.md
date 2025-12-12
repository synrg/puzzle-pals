# puzzle-pals

A collection of scripts to facilitate group puzzle play.

- [randompuz.py](#randompuzpy)
    - A random jigsaw puzzle base image URL generator

## Installation

- [Install uv](#install-uv)
- Clone this repo:
```sh
$ git clone https://github.com/synrg/puzzle-pals
```

### Install uv

Follow the instructions at https://docs.astral.sh/uv/getting-started/installation/
to install `uv` for your operating system.

## Usage

- Run each script with uv, e.g.
```sh
$ cd puzzle-pals
$ uv run randompuz
```

## Scripts

### randompuz.py

A random jigsaw puzzle base image URL generator.

#### Usage

```sh
$ uv run randompuz [lowest-image-number] [highest-image-number]
```

- **lowest-image-number** (optional)
    - default: 1
    - subtracted from <code>highest-image-number</code> if negative
- **highest-image-number** (optional)
    - default: first image # at https://jigsawpuzzles.io/browse/latest

#### Examples

Any random puzzle image:

```sh
$ uv run randompuz
```

Any of the latest 200 puzzle images:

```sh
$ uv run randompuz -200
```
