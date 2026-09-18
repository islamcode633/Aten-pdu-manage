#!/usr/bin/env python3

"""
Utility for remote management of ATEN PDUs.
"""

import sys
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from argparse import ArgumentParser, Namespace
from telnetlib3.sync import TelnetConnection

from exceptions import ErrorOptionsNotFound, ErrorInvalidArgForOption
from constants import User, OUTLETS, OPTIONS


P = ParamSpec('P')
R = TypeVar('R')


def validate(func: Callable[P, R]) -> Callable[P, R]:
    """ Verification of transmitted parameters """
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        for param, value in kwargs.items():
            if value in OUTLETS or value in OPTIONS:
                continue
            raise ErrorInvalidArgForOption(f"Invalid argument [{value}] for option [{param}]")
        return func(*args, **kwargs)
    return wrapper


class AtenPDU:
    """ PDU device implementation """
    _user: User = User()
    _host: str = '192.168.0.60'

    @classmethod
    def _auth(cls, conn: TelnetConnection) -> None:
        """ Authorization on the PDU how User(adm) """
        conn.write(cls._user.login)
        conn.write(cls._user.password)

    @classmethod
    def _send_command(cls, command: str) -> str | bytes:
        """ Private API for sending commands to the PDU """
        with TelnetConnection(host=cls._host) as conn:
            cls._auth(conn)
            conn.write(command + '\r\n')
            result: str | bytes = conn.read()
        return result

    @staticmethod
    @validate
    def status(outlet: str) -> str | bytes:
        """ Checking status outlet """
        return AtenPDU._send_command(f"read status {outlet} format")

    @staticmethod
    @validate
    def power(outlet, control, option: str) -> str | bytes:
        """ Manage power supply """
        return AtenPDU._send_command(f"sw {outlet} {control} {option}")

    @staticmethod
    @validate
    def reboot(outlet: str) -> str | bytes:
        """ Power outlet reboot """
        return AtenPDU._send_command(f"sw {outlet} reboot")

    @staticmethod
    @validate
    def measure(option: str) -> str | bytes:
        """ Get the current state """
        return AtenPDU._send_command(f"read meter dev {option} format")


def parser() -> Namespace:
    """ Command-line argument parsing """
    parse: ArgumentParser = ArgumentParser(description='For remote control of the Aten power distribution unit.')
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


def dispatchering(pdu: AtenPDU, args: Namespace) -> None:
    """ Command manager """
    o: str = args.outlet
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


if __name__ == '__main__':
    try:
        ERR_MSG: ErrorOptionsNotFound | ErrorInvalidArgForOption | None = None
        dispatchering(pdu=AtenPDU(), args=parser())
    except (ErrorOptionsNotFound, ErrorInvalidArgForOption) as e:
        ERR_MSG = e
    finally:
        if not ERR_MSG:
            sys.exit(0)
        sys.exit(f"error: {ERR_MSG}")


# handler() input from console for change log, pass, ip
# unittest for aten_pdu_cli
# add submodul command after exec
# add TUI
