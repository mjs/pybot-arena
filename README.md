# PyBot Arena

In this game, players implement an algorithm - called a "Bot" - which controls
an autonomous tank in Python. The Bots from different players then compete them
against each other. A number of bots can be active in a single match at the
same time.

XXX screenshot

The game borrows code and assets from
[PaulleDemon/Hunter2](https://github.com/PaulleDemon/Hunter2) but has been
heavily modified.

## Installation

Create a virtual environment using your preferred approach and activate it, for
example:

```
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies using your preferred tooling, for example:

```
pip install -r requirements.txt
```

The commands will vary if for example you're using [pip-tools][1] or [uv][2],
but if you're using those tools you probably know what to do.

[1]: https://github.com/jazzband/pip-tools
[2]: https://github.com/astral-sh/uv


## Running a Match

PyBot Arena needs to be told where to find the implementations for the bots
which control each tank, and which to play against each other for a particular
game. This is specified on the command line.

There are some simple bot implementations in the `sample_bots.py` module.

To run a match with one Random and one Basic bot:

```
python sample_bots.Random sample_bots.Basic
```

Bots have a default name which can be overridden on the command line. For
example, to give the Basic bot a name of "foo":

```
python sample_bots.Random sample_bots.Basic,foo
```

Bots also have a default color which can be overridden on the command line. For
example, to give the Basic bot a name of "foo" and force it to be yellow:

```
python sample_bots.Random sample_bots.Basic,foo,yellow
```

Any [PyGame color][3] name can be used for a tank color.

[3]: https://www.pygame.org/docs/ref/color_list.html

## Creating a Bot

Bots must be created in a Python module which is accessible to PyBot Arena.
Each Bot is a should be a subclass of the `bot.Bot` class and should implement
the `default_name`, `default_color` and `next` method.

The game engine will repeatedly call the `next` method of each Bot to progress
the match. The `state` argument to `next` provides relevant details
about the tank's position, angle and speed as well as details about other
nearby tanks and bullets(!). 

Each call to `next` should return an `Action` instance (see `bots.py`) to
change the tank's speed or angle, or to fire a bullet. None should be returned
if the tank should continue doing what it's already doing.

See `bots.py` and `sample_bots.py` for further details and inspiration.

Good luck!

### Tips

- CurrentState includes a `collision` flag which indicates that the tank has
  just run into something. It can be useful to change direction when this
  happens.
- The `relative_angle` field of NearbyBot instances is useful for targeting
  other tanks.
- The list of `nearby_bullets` is handy for taking evasive action.

