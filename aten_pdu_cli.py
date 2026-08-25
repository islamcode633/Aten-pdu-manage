#!/usr/bin/env python3

"""
...
"""

import sys
from dataclasses import dataclass
from functools import wraps

from telnetlib3.sync import TelnetConnection


# Enum()
OUTLETS = {
    '1':'o01', '2':'o02', '3':'o03', '4':'o04',
    '5':'o05', '6':'o06', '7':'o07', '8':'o08',
}

PATTERN = (
    'simple', 'format',
    'imme', 'delay',
    'on', 'off'
)

OPTIONS = ()


class ErrorValidArg(Exception):
    """ ... """


def validate(func):
    """ ... """
    @wraps(func)
    def wrapper(outlet, ret_str):
        #if outlet in OUTLETS and ret_str in ('simple', 'format'):
        result = func(outlet, ret_str)
        return result
        #raise ErrorValidArg("Error: Invalid arguments !")
    return wrapper


@dataclass(frozen=True)
class User:
    """ ... """
    login: str = 'administrator\r\n'
    password: str = 'password\r\n'


class AtenPDU:
    """ ... """
    user = User()
    host = '192.168.0.60'

    @classmethod
    def _auth(cls, conn):
        conn.write(cls.user.login)
        conn.write(cls.user.password)

    @classmethod
    def _send_command(cls, command):
        """ ... """
        with TelnetConnection(host=pdu.host) as conn:
            cls._auth(conn)
            conn.write(command + '\r\n')
            result = conn.read()
        return result

    @staticmethod
    @validate
    def status(outlet, ret_str):
        """ ... """
        return AtenPDU._send_command(f"read status {outlet} {ret_str}")

    @staticmethod
    @validate
    def power(outlet, control, option):
        """ ... """
        return AtenPDU._send_command(f"sw {outlet} {control} {option}")

    @staticmethod
    def reboot(outlet):
        """ ... """
        return AtenPDU._send_command(f"sw {outlet} reboot")

    @staticmethod
    def measure(option):
        """ ... """
        return AtenPDU._send_command(f"read meter dev {option} format")


try:
    pdu = AtenPDU()

    print(pdu.status('o08', 'simple'))
    print(pdu.measure('pow'))
except ErrorValidArg as e:
    sys.exit(f"{e}")
