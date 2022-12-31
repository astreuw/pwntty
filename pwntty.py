#!/usr/bin/env python3

from random import randint
from termios import TIOCSTI
from time import sleep

import argparse
import fcntl
import os
import sys

VERBOSE = False
BANNER = r'''
                  .         *    .            *          .----. .
 '  ____               ______________  __    .---------. | == |
   / __ \_   "  ______/_  __/_  __/\ \/ /    |.-"""""-.| |----|
  / /_/ / | /| / / __ \/ /   / /    \  /     ||       || | == |
 / ____/| |/ |/ / / / / /   / / ,   / / *    ||       || |----|
/_/     |__/|__/_/ /_/_/   /_/     /_/       |'-.....-'| |::::|
,                                            `"")---(""` |____|
    Created by @astreuzz                    /:::::::::::\" \'\
'''

print(BANNER)


def send_input(dev, data):
    for ch in data:
        fcntl.ioctl(dev, TIOCSTI, ch)


def write(dev, data):
    os.write(dev, data.encode())


def bug_tty_cursor(dev, cur):
    codes = lambda ch, n: f"{ch}\033[XZ".replace(
        "X", str(n)).replace("Z", list("ABCD")[randint(0, 3)])

    cur = cur.split()
    try:
        printv("+ Bug cursor started...")
        while True:
            for ch in cur:
                write(dev, codes(ch, randint(0, 0x7f)))
    except KeyboardInterrupt:
        print("- Bug cursor stopped (CTL + C)", file=sys.stderr)


def lock_tty_io(dev):
    cmd = "exec 2>&-\nclear\nexec >&-"
    send_input(dev, cmd)
    write(dev, "\033[9C")
    printv(f"* The device '{dev}' was locked")


def parse_args():
    parser = argparse.ArgumentParser(
        prog="pwntty",
        description="A toolkit to control TTY devices")

    parser.add_argument(
        "devices",
        nargs="+",
        help="Target TTY device",
        metavar="DEVICES")

    parser.add_argument(
        "-e", "--exec",
        nargs="?",
        help="Run a given command line on target",
        metavar="CMD")

    parser.add_argument(
        "-m", "--message",
        nargs="?",
        help="Send a message to target")

    parser.add_argument(
        "-b", "--bug-cursor",
        nargs="?",
        default="",
        help="Turn on the bug cursor on target",
        metavar="STR")

    parser.add_argument(
        "-l", "--lock-tty",
        action="store_true")

    parser.add_argument(
        "-v", "--verbose",
        action="store_true")

    return parser.parse_args()


def printv(*msg):
    if VERBOSE:
        print(*msg)


def main():
    args = parse_args()
    devices = []

    global VERBOSE
    VERBOSE = args.verbose

    if not os.getuid() == 0:
        print("error: pwntty must be run as root", file=sys.stderr)
        exit(1)

    printv("* Checking devices...")
    for dev in args.devices:
        try:
            fd = os.open(dev, os.O_RDWR)
            devices.append(fd)
            printv(f"+ The device '{dev}' is OK!")
        except Exception as e:
            print(f"- {e}", file=sys.stderr)

    for dev in devices:
        if args.exec:
            send_input(dev, args.exec + "\n")

        if args.message:
            for ch in args.message:
                write(dev, ch)
                sleep(0.05)

        if args.bug_cursor:
            bug_tty_cursor(dev, cur=args.bug_cursor)

        if args.lock_tty:
            lock_tty_io(dev)


if __name__ == "__main__":
    main()
