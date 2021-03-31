# botele
### Python Telegram Bot Factory

## Installation
```bash
$ pip install botele
```
## Basic Usage
```bash
$ mkdir mybot
$ cd mybot
$ botele setup .
$ echo "<BOT TOKEN>" > mybot.token
$ vim mybot.py # Write your bot file
...
$ botele make # Checks for bot consistency
$ botele install
$ botele list
Available bots:
         1. mybot
$ botele run mybot # Here we go!
> Started Polling, going idle.
```
