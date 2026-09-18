#!/usr/bin/env python3

"""
Unit test for decorator
"""

from aten_pdu_cli import validate


class TestDecorator:
    """ Decorator check """
    @staticmethod
    @validate
    def test1(arg: str) -> str:
        """ test1 """
        return arg

    @staticmethod
    @validate
    def test2(arg: str, arg2: str, arg3: str) -> tuple[str, str, str]:
        """ test2 """
        return arg, arg2, arg3

    @staticmethod
    @validate
    def test3(arg: str) -> str:
        """ test3 """
        return arg

    @staticmethod
    @validate
    def test4(arg: str, arg2: str) -> tuple[str, str]:
        """ test4 """
        return arg, arg2


def running_positive_tests():
    """ entry point """
    mock: TestDecorator = TestDecorator()

    assert mock.test2(arg='o08', arg2='curr', arg3='pow') == ('o08', 'curr', 'pow')
    assert mock.test3(arg='volt') == 'volt'
    assert mock.test4(arg='o01', arg2='imme') == ('o01', 'imme')


running_positive_tests()
