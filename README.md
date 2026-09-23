# deploy
git clone https://github.com/islamcode633/Aten-pdu-manage.git
Note: if not installed python3-venv -> sudo apt install python3-venv -y
python3 -m venv Aten-pdu-manage && cd Aten-pdu-manage && source bin/activate

# how use
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
