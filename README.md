# AvroAiro
BSides Presentation: Jumping Airgaps with Networkless Exfiltration

![oob-fram-vs-wlan drawio (1)](https://github.com/user-attachments/assets/38563265-764a-4beb-9d37-553598e3fdae)

## Overview - what is this?
AvroAiro is a tool that was created to exfiltrate data via Probe Requests (PRQs).

### Why is this different?
This is different because monitor mode is not required on the victim to perform this exfiltration.

To intercept probe requests sent from victim devices, the attacker (or listener) needs to have monitor mode.
This is because probe requests are management frames, which are out-of-band.

### Important Disclaimer
This tool should be used responsibly, and is showcased as a proof of concept.
Anyone using this tool is assumed to abide by applicable laws.

### Other Important Disclaimer
Edit the scripts, and carefully read through the code. If you run them as-is, there will be errors
This is a PoC, it's not carefully vetted code that works out of the box.

### Requirements
- Administrator / sudo privileges on both attacker and victim
- Powershell with regedit privileges
- aircrack-ng
- pcap
- scapy

## PoC Video
[![IMAGE ALT TEXT](http://img.youtube.com/vi/o7vZTud8kz0/0.jpg)](https://www.youtube.com/watch?v=o7vZTud8kz0)

### On Attacker Machine:
- Make sure the the proper channel and band is selected.
```
sudo airmon-ng check
sudo airmon-ng check kill
sudo airmon-ng start <wlan-adapter> <channel>
```
- Note: make sure to change the octets in the identifer, otherwise it will default to "BE:EF:FF"
```
sudo python3 avroairo_listener.py
```
### On victim machine (windows):
- Currently the exfiltrated message is hardcoded in the script
- Change this line in the script: "REG_KEY_PATH = "HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{WNIC-UUID}\\0000" #<-- Change this!
```
sudo python3 avroairo_sender.py
```

