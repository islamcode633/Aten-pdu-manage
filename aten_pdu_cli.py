#!/usr/bin/env python3

"""
...
"""

import sys
from dataclasses import dataclass
from functools import wraps
#typing
from argparse import ArgumentParser

from telnetlib3.sync import TelnetConnection


OUTLETS = (
    'o01', 'o02', 'o03', 'o04',
    'o05', 'o06', 'o07', 'o08')

OPTIONS = (
    'format', 'imme', 'delay', 'on', 'off',
    'curr', 'volt', 'pow', 'pd', 'freq')


class ErrorOptionsNotFound(Exception):
    """ ... """

class ErrorInvalidArgForOption(Exception):
    """ ... """


def validate(func):
    """ ... """
    @wraps(func)
    def wrapper(**kwargs):
        for param, value in kwargs.items():
            if value in OUTLETS or value in OPTIONS:
                continue
            raise ErrorInvalidArgForOption(f"Invalid argument [ {value} ] for option [ {param} ]")
        result = func(**kwargs)
        return result
    return wrapper


@dataclass(frozen=True)
class User:
    """ ... """
    login: str = 'administrator\r\n'
    password: str = 'password\r\n'


class AtenPDU:
    """ ... """
    _user = User()
    _host = '192.168.0.60'

    @classmethod
    def _auth(cls, conn):
        conn.write(cls._user.login)
        conn.write(cls._user.password)

    @classmethod
    def _send_command(cls, command):
        """ ... """
        with TelnetConnection(host=cls._host) as conn:
            cls._auth(conn)
            conn.write(command + '\r\n')
            result = conn.read()
        return result

    @staticmethod
    @validate
    def status(outlet):
        """ ... """
        return AtenPDU._send_command(f"read status {outlet} format")

    @staticmethod
    @validate
    def power(outlet, control, option):
        """ ... """
        return AtenPDU._send_command(f"sw {outlet} {control} {option}")

    @staticmethod
    @validate
    def reboot(outlet):
        """ ... """
        return AtenPDU._send_command(f"sw {outlet} reboot")

    @staticmethod
    @validate
    def measure(option):
        """ ... """
        return AtenPDU._send_command(f"read meter dev {option} format")


def parser():
    """ ... """
    parse = ArgumentParser(description='For remote control of the Aten power distribution unit.')
    parse.add_argument('exec', help='')
    parse.add_argument('-s', '--status', action='store_true',
                       help='check the condition of the outlet on/off.\n' \
                       ' Used with [ --outlet ]')
    parse.add_argument('-p', '--power', action='store_true',
                       help='turn the outlet on/off.\n' \
                       ' Used with [ --outlet, --control, --option ]')
    parse.add_argument('-r', '--reboot', action='store_true',
                       help='switch outlet off and then switch outlet on.\n' \
                       ' Used with [ --outlet ]')
    parse.add_argument('-m', '--measure', action='store_true',
                       help='displays power measurement values.\n' \
                       ' Used with [ --option ]')

    parse.add_argument('-out', '--outlet', help='outlet number from o01 to o08')
    parse.add_argument('-c', '--control', help='params on/off')
    parse.add_argument('-o', '--option',
                       help='example:' \
                       ' imme - switch outlet status immediately,' \
                       ' curr - read current measurement.' \
                       ' other options freq/delay etc ...')
    parse.add_argument('--print', action='store_true',
                       help='print all supported options')
    return parse.parse_args()

def dispatchering(pdu, args):
    """ ... """
    o = args.outlet
    stdout = sys.stdout.write

    if args.status:
        stdout(pdu.status(outlet=o) + '\n')
    elif args.power:
        stdout(pdu.power(outlet=o, control=args.control, option=args.option) + '\n')
    elif args.reboot:
        stdout(pdu.reboot(outlet=o) + '\n')
    elif args.measure:
        stdout(pdu.measure(option=args.option) + '\n')
    elif args.print:
        stdout(f"{OPTIONS}\n")
    else:
        raise ErrorOptionsNotFound('Required option --status|--power|--reboot|--measure|--print')

def main():
    """ ... """
    try:
        err_msg = None
        dispatchering(pdu=AtenPDU(), args=parser())
    except (ErrorOptionsNotFound, ErrorInvalidArgForOption) as e:
        err_msg = e
    finally:
        if not err_msg:
            sys.exit(0)
        sys.exit(f"error: {err_msg}")


if __name__ == '__main__':
    main()


# handler() input from console for change log, pass, ip
# mb add parser output data
# unittest dispatch() handler()
# typing
# refactor
# decomposite module
