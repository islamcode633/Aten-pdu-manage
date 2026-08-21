#!/usr/bin/env python3

"""
...
"""

import sys
from telnetlib3.sync import TelnetConnection


OUTLETS = {
    '1':'o01', '2':'o02', '3':'o03', '4':'o04',
    '5':'o05', '6':'o06', '7':'o07', '8':'o08',
}


class ErrorValidArg(Exception):
    """ ... """

class ErrorFlag(Exception):
    """ ... """


class AtenPDU:
    """ ... """
    def __init__(self) -> None:
        self.login: str = 'administrator'
        self.password: str = 'password'
        self.host: str = '192.168.0.60'

    def _send_command(self, command: str):
        """ ... """
        chars_control_input = '\r\n'
        with TelnetConnection(host=self.host) as conn:
            # auth
            conn.write(self.login + chars_control_input)
            conn.write(self.password + chars_control_input)
            conn.write(command + chars_control_input)
            result = conn.read()
        return result

    def status(self, outlet, ret_str):
        """ ... """
        if ret_str in ('simple', 'format'):
            return self._send_command(f"read status {outlet} {ret_str}")
        raise ErrorFlag("Error: Valid argument, but with the wrong flag !")

    def power(self, outlet, control, option):
        """ ... """
        if control in ('on', 'off') and option in ('imme', 'delay'):
            return self._send_command(f"sw {outlet} {control} {option}")
        raise ErrorFlag("Error: Valid argument, but with the wrong flag !")

    def reboot(self, outlet):
        """ ... """
        return self._send_command(f"sw {outlet} reboot")


def validate(pattern):
    """ ... """
    if (pattern := pattern.strip()) in ('simple', 'format', 'imme', 'delay', 'on', 'off'):
        return pattern
    raise ErrorValidArg("Error: Invalid arguments !")


try:
    pdu = AtenPDU()
    print(pdu.status(outlet=OUTLETS['8'], ret_str=validate('simple')))
    print(pdu.power(outlet=OUTLETS['8'], control=validate('off'), option=validate('imme')))
    print(pdu.power(outlet=OUTLETS['8'], control=validate('on'), option=validate('delay')))
except (ErrorValidArg, ErrorFlag) as e:
    sys.exit(f"{e}")


# usage()
# simply argsparse
# exceptions
# unit tests
# logger
