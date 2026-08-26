#!/usr/bin/env python3

"""
...
"""

import sys
from dataclasses import dataclass
from functools import wraps
#typing
#logger

from telnetlib3.sync import TelnetConnection


# Enum()
OUTLETS = (
    'o01', 'o02', 'o03', 'o04',
    'o05', 'o06', 'o07', 'o08')

OPTIONS = (
    'simple', 'format', 'imme', 'delay', 'on', 'off',
    'curr', 'volt', 'pow', 'pd', 'freq')


class ErrorValidArg(Exception):
    """ ... """


def validate(func):
    """ ... """
    @wraps(func)
    def wrapper(**kwargs):
        for param, value in kwargs.items():
            if value in OUTLETS or value in OPTIONS:
                continue
            #logger({func.__name__}({param}={value} + docstring))
            raise ErrorValidArg(f"Error: Invalid arguments !")
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
    user = User()
    host = '192.168.0.60'

    @classmethod
    def _auth(cls, conn):
        conn.write(cls.user.login)
        conn.write(cls.user.password)

    @classmethod
    def _send_command(cls, command):
        """ ... """
        with TelnetConnection(host=cls.host) as conn:
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
    @validate
    def reboot(outlet):
        """ ... """
        return AtenPDU._send_command(f"sw {outlet} reboot")

    @staticmethod
    @validate
    def measure(option):
        """ ... """
        return AtenPDU._send_command(f"read meter dev {option} format")


try:
    pdu = AtenPDU()

    print(pdu.status(outlet='o03', ret_str='simple'))
    print(pdu.power(outlet='o08', control='on', option='imme'))
    print(pdu.reboot(outlet='o08'))
    print(pdu.measure(option='curr'))

except ErrorValidArg as e:
    sys.exit(f"{e}")
