#!/usr/bin/env python3

"""
Unit test for decorator
"""

from aten_pdu_cli import validate


class TestDecorator:
    """ Decorator check """

    @staticmethod
    @validate
    def test1(arg):
        """ ... """
        return arg

    @staticmethod
    @validate
    def test2(arg, arg2, arg3):
        """ ... """
        return arg, arg2, arg3

    @staticmethod
    @validate
    def test3(arg):
        """ ... """
        return arg

    @staticmethod
    @validate
    def test4(arg, arg2):
        """ ... """
        return arg, arg2

def running_positive_tests():
    """ ... """
    mock = TestDecorator()

    mock.test1(arg='simple')
    mock.test2(arg='o08', arg2='curr', arg3='pow')
    mock.test3(arg='volt')
    mock.test4(arg='o01', arg2='imme')


running_positive_tests()
