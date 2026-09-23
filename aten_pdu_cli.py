#!/usr/bin/env python3

"""
Utility for remote management of ATEN PDUs.
"""

from argparse import ArgumentParser, Namespace

from exceptions import ErrorOptionsNotFound, ErrorInvalidArgForOption
from constants import OPTIONS, STDOUT, SUCCESS_CODE, FAILED_CODE, EXIT
from lib import AtenPDUClient, read_cfg


def parser() -> Namespace:
    """ Command-line argument parsing """
    parse: ArgumentParser = ArgumentParser(description='For remote control of the Aten power distribution unit.')
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


def dispatchering(pdu_client: AtenPDUClient, args: Namespace) -> None:
    """ Command manager """
    o: str = args.outlet

    if args.status:
        STDOUT(pdu_client.status(outlet=o) + '\n')
    elif args.power:
        STDOUT(pdu_client.power(outlet=o, control=args.control, option=args.option) + '\n')
    elif args.reboot:
        STDOUT(pdu_client.reboot(outlet=o) + '\n')
    elif args.measure:
        STDOUT(pdu_client.measure(option=args.option) + '\n')
    elif args.print:
        STDOUT(f"{OPTIONS}\n")
    else:
        raise ErrorOptionsNotFound('Required option --status|--power|--reboot|--measure|--print')


if __name__ == '__main__':
    try:
        dispatchering(pdu_client=AtenPDUClient(*read_cfg()), args=parser())
        EXIT(SUCCESS_CODE)
    except (ErrorOptionsNotFound, ErrorInvalidArgForOption) as e:
        STDOUT(f"Error: {e}\n")
        EXIT(FAILED_CODE)
    except Exception as e:
        STDOUT(f"Error: {e}\n")
        EXIT(FAILED_CODE)
