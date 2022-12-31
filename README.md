# pwntty

Pwntty is an open source project to control other terminals on your machine. Mainly focused on real time CTF games (KoTH, Battlegrounds, etc), pwntty has several features for fun.

Installation
----

Download pwntty by cloning the [Git](https://github.com/astreuzz/pwntty.git) repository:
```
git clone https://github.com/astreuzz/pwntty pwntty
```

Usage
----

To get a list of basic options use:
```
# python pwntty.py -h
```

Some of pwntty options:
```
usage: pwntty [-h] [-e [CMD]] [-m [MESSAGE]] [-b [STR]] [-l] [-v]
              DEVICES [DEVICES ...]

A toolkit to control TTY devices

positional arguments:
  DEVICES               Target TTY device

options:
  -h, --help            show this help message and exit
  -e [CMD], --exec [CMD]
                        Run a given command line on target
  -m [MESSAGE], --message [MESSAGE]
                        Send a message to target
  -b [STR], --bug-cursor [STR]
                        Turn on the bug cursor on target
  -l, --lock-tty
  -v, --verbose

```

Requirements
----
- Python3.0+

# License
MIT License

Copyright (c) 2022 Ricardo Costa
