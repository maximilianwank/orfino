# orfino
This Python package contains a notification service for filled orders on crypto exchanges.

If you want to benefit while trading and additionally support the development of this tool, consider to use my referral 
links to the exchanges I use the most:

* [Binance](https://accounts.binance.com/en/register?ref=80028974): Referral ID 80028974
* [Kucoin](https://www.kucoin.com/ucenter/signup?rcode=r3L3UJ8): Referral Code r3L3UJ8

## :electric_plug: Installation

Assuming [pip](https://pip.pypa.io/) and [git](https://git-scm.com/) available on your system, just use

```
pip install git+https://github.com/maximilianwank/orfino.git
```

It is recommended to use some virtual environment like [venv](https://docs.python.org/3/library/venv.html) or others.


## :gear: Configuration

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

## :running: Run the program

One can start the program with the command line using its module name. 
Note that you must pass the path to your config file as argument:

```
python3 -m orfino /path/to/your/config.ini
```
