#!/usr/bin/env bash

set -x

### Generate new password
new_password=$(base64 < /dev/urandom | tr -d 'O0Il1+/' | head -c 8; printf '\n')

### SSH to MikroTik and update the password for 'sre_g' Wi-Fi network
ssh mikrotik "/interface/wireless/security-profiles/set wifi_guest wpa2-pre-shared-key=${new_password}"

### Create QR Code using the newly created password
qrencode -t ASCII -m 0 -o qr_ascii.txt 'WIFI:S:sre_g;T:WPA2;P:'"${new_password}"';;'

### Add double quotes around each line and a comma at the end
sed -i -e 's/\(.*\)/    "\1",/' qr_ascii.txt
### Duplicate each line
sed -i -e '/\(.*\)/p' qr_ascii.txt

### Update 'qr_code' list of strings in 'main.py'
sed -i -e '/# qr_code_start/,/# qr_code_end/c\# qr_code_start\n# qr_code_end' main.py
sed -i -e '/# qr_code_start/r qr_ascii.txt' main.py

### Use 'rshell' to copy 'main.py' and 'reset_pico.py' to Raspberry Pi Pico
rshell 'cp main.py reset_pico.py /pyboard/; repl ~ import reset_pico ~'

