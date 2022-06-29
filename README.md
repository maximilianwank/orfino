# orfino
This Python package contains a notification service for filled orders on crypto exchanges.

## :electric_plug: Installation

Assuming [pip](https://pip.pypa.io/) and [git](https://git-scm.com/) available on your system, just use

```
pip install git+https://github.com/maximilianwank/orfino.git
```

It is recommended to use some virtual environment like [venv](https://docs.python.org/3/library/venv.html) or others.


## :page_facing_up: Configuration

A full config sample would be the following:

```
[binance]
key = foo
secret = bar

[notifymydevice]
key = baz

[timedrotatingfile]
filename = orfino.log
count = 14
when = D
```
