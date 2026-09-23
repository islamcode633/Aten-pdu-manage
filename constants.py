"""
Сontains the following constants
    :OUTLETS: outlets numbers from 1 to 8
    :OPTIONS: supported options on PDU device
"""

import sys
import typing


OUTLETS: typing.Final[tuple[str, ...]] = (
    'o01', 'o02', 'o03', 'o04',
    'o05', 'o06', 'o07', 'o08',)

OPTIONS: typing.Final[tuple[str, ...]] = (
    'format', 'imme', 'delay', 'on', 'off',
    'curr', 'volt', 'pow', 'pd', 'freq',)

SUCCESS_CODE: typing.Final[int] = 0
FAILED_CODE: typing.Final[int] = 1

STDOUT = sys.stdout.write
EXIT = sys.exit
