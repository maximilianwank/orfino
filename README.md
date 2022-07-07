# orfino
This Python package contains a notification service for filled orders on crypto exchanges.

If you want to benefit while trading and additionally support the development of this tool, consider to use my referral 
links to the exchanges I use the most:

* [Binance](https://accounts.binance.com/en/register?ref=80028974): Referral ID 80028974
* [Kucoin](https://www.kucoin.com/ucenter/signup?rcode=r3L3UJ8): Referral Code r3L3UJ8

## :warning: Disclaimer

Please note that this tool comes without any kind of warranty.

## :electric_plug: Installation

Assuming [pip](https://pip.pypa.io/) being available on your system, just use

```
pip install https://github.com/maximilianwank/orfino/archive/refs/heads/main.zip
```

It is recommended to use some virtual environment like [venv](https://docs.python.org/3/library/venv.html) or others.

## :gear: Configuration

A config sample would be the following:

```
[binance]
key = foo
secret = bar

[kucoin]
key = foo
secret = bar
password = baz

[notifymydevice]
key = foo

[timedrotatingfile]
filename = orfino.log
count = 14
when = midnight
```

With `;` you can comment sections.

### :currency_exchange: Exchanges

Exchanges can be added by a section with the name of the exchange and different keys like `key` (for an API key), 
`secret` (for the API secret) and an optional `password`. Using [ccxt](https://github.com/ccxt/ccxt) for the API calls, 
in theory [many exchanges](https://github.com/ccxt/ccxt#certified-cryptocurrency-exchanges) are supported. However, 
only Binance and Kucoin have been tested. Please feel free to reach out if you want exchanges to be added.

### :bell: Notify My Device

Notifications on filled orders can be sent via [Notify My Device](https://www.notifymydevice.com/). You just have to 
register and install the app on your respective device.

### :card_file_box: Timed Rotating File Logger

You can use a timed rotating file logger to save a log of various messages. Have a glance on the official 
[Python docs](https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler). The supported keys are 
`filename`, `count` (for `backupCount`) and `when`.

## :running: Run the program

One can start the program with the command line using its module name. 
Note that you must pass the path to your config file as argument:

```
python3 -m orfino /path/to/your/config.ini
```
