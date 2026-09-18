"""
Сontains the following constants
    :User: adm user
    :OUTLETS: outlets numbers from 1 to 8
    :OPTIONS: supported options on PDU device
"""

import typing
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """ User with administrator privileges """
    login: str = 'administrator\r\n'
    password: str = 'password\r\n'


OUTLETS: typing.Final[tuple[str, ...]] = (
    'o01', 'o02', 'o03', 'o04',
    'o05', 'o06', 'o07', 'o08',)

OPTIONS: typing.Final[tuple[str, ...]] = (
    'format', 'imme', 'delay', 'on', 'off',
    'curr', 'volt', 'pow', 'pd', 'freq',)
