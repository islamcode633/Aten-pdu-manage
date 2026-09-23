"""
The module contains an implementation of the ATEN PDU device and
 auxiliary objects.

  :validate: command-line argument validation
  :read_cfg: reads the configuration from a file to obtain the login, password
    and IP address of the PDU device.
  :AtenPDUClient: PDU Client Implementation
"""

from functools import wraps
from typing import Callable, ParamSpec, TypeVar
from telnetlib3.sync import TelnetConnection

from exceptions import ErrorInvalidArgForOption
from constants import OUTLETS, OPTIONS


P = ParamSpec('P')
R = TypeVar('R')


def validate(func: Callable[P, R]) -> Callable[P, R]:
    """ Verification of transmitted parameters """
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        for param, value in kwargs.items():
            if value in OUTLETS or value in OPTIONS:
                continue
            raise ErrorInvalidArgForOption(f"Invalid argument [{value}] for [{param}]")
        return func(*args, **kwargs)
    return wrapper


def read_cfg() -> tuple[str, str, str]:
    """ Reads the configuration from expected file pdu.cfg """
    try:
        with open('pdu.cfg', encoding='utf-8', mode='r') as f:
            config: list[str] = [string.strip().split()[-1] for string in f]
            login, password, host = config[0], config[1], config[2]
            return login, password, host
    except (IndexError, OSError) as e:
        raise RuntimeError('Failed to read configuration from [ pdu.cfg ]') from e


class AtenPDUClient:
    """ PDU Client Implementation """

    def __init__(self, login: str, password: str, host: str):
        """
        :login: username
        :password: password
        :host: ip addr pdu
        """
        self.login: str = login
        self.password: str = password
        self.host: str = host

    def _send_command(self, command: str) -> str | bytes:
        """ Sending commands to the PDU """
        with TelnetConnection(host=self.host) as conn:
            conn.write(f"{self.login}\r\n")
            conn.write(f"{self.password}\r\n")
            conn.write(f"{command}\r\n")
            return conn.read()

    @validate
    def status(self, outlet: str) -> str | bytes:
        """ Checking status outlet """
        return self._send_command(f"read status {outlet} format")

    @validate
    def power(self, outlet, control, option: str) -> str | bytes:
        """ Manage power supply """
        return self._send_command(f"sw {outlet} {control} {option}")

    @validate
    def reboot(self, outlet: str) -> str | bytes:
        """ Power outlet reboot """
        return self._send_command(f"sw {outlet} reboot")

    @validate
    def measure(self, option: str) -> str | bytes:
        """ Get the current state """
        return self._send_command(f"read meter dev {option} format")
