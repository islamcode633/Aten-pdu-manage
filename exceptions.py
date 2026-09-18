"""
Errors encountered during unexpected operation of aten_pdu_cli
"""


class ErrorOptionsNotFound(Exception):
    """ An error occurs if mandatory commands are not specified """


class ErrorInvalidArgForOption(Exception):
    """ An error occurs if the passed options were incorrect """
