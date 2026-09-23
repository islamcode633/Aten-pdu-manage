# ATEN PDU Remote Manager
A simple and efficient Python-based command-line interface (CLI) utility for remotely managing ATEN Power Distribution Units (PDUs) via Telnet. It allows you to check outlet status, control power, reboot outlets, and retrieve energy consumption data.

## Features
*   🔍 **Checking status**: a specific outlet is switched on or off.
*   ⚡ **Power management**: remote switching of electrical outlets on and off.
*   🔄 **Reboot**: rapidly cycling power off and on to reboot connected equipment.
*   📊 **Monitoring**: obtaining data on voltage (Volt), current (Curr), power (Pow), and frequency (Freq).
*   🛠 **Simple interface**: control via command-line flags.

# Deploy (Debian/Ubuntu)
* sudo apt update && sudo apt install python3-venv git -y
* git clone https://github.com/islamcode633/Aten-pdu-manage.git
* python3 -m venv Aten-pdu-manage && cd Aten-pdu-manage && source bin/activate

# Using
See ./aten_pdu_cli.py -h for more details.
example command:
    # support options
    ./aten_pdu_cli.py --print

    # check work status outlet 8
    ./aten_pdu_cli.py [ -s | --status ] -out o08

    # after off immediately on outlet 8
    ./aten_pdu_cli.py [ -r | --reboot ] -out o08

    # immediate disconnection of outlet 8
    ./aten_pdu_cli.py [ -p | --power ] [ -out | --outlet ] o08 [ -c | --control ] off [ -o | --option ] imme


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
