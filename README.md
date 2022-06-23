# orfino
This Python package contains a notification service for filled orders on crypto exchanges.

## Configuration
A full config sample would be the following:
```
[binance]
key = foo
secret = bar

[notifymydevice]
key = baz

[timedrotatingfile]
filename = orfino.log
count = 90
when = D
```
