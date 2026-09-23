# ATEN PDU Remote Manager
Простая и эффективная CLI-утилита на Python для удаленного управления блоками распределения питания (PDU) производства **ATEN** через протокол Telnet. Позволяет проверять статус розеток, управлять питанием, перезагружать их и снимать показатели электроэнергии.

## Features
*   🔍 **Checking status**: Узнать, включена или выключена конкретная розетка.
*   ⚡ **Power management**: Дистанционное включение/выключение розеток.
*   🔄 **Reboot**: Быстрое циклическое выключение и включение для перезагрузки подключенного оборудования.
*   📊 **Monitoring**: Получение данных о напряжении (Volt), силе тока (Curr), мощности (Pow) и частоте (Freq).
*   🛠 **Simple interface**: Управление через привычные флаги командной строки.

# Deploy (Debian/Ubuntu)
sudo apt update && sudo apt install python3-venv git -y
git clone https://github.com/islamcode633/Aten-pdu-manage.git
python3 -m venv Aten-pdu-manage && cd Aten-pdu-manage && source bin/activate

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
