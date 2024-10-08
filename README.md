# Neutrino
Work in progress name: Jumping Airgaps with Networkless Exfiltration

### Requirements
- Powershell
- aircrack-ng
- pcap
- scapy

## Neutrino Usage
```
python neutrino-shell.py -h

usage:

options:


```
### On Attacker Machine:
- Make sure the the proper channel and band is selected.
```
sudo airmon-ng check
sudo airmon-ng check kill
sudo airmon-ng start <wlan-adapter> <channel>
sudo python3 neutrino-shell.py
```
### On victim machine (windows):
- Currently the exfiltrated message is hardcoded in the script
```
python neutrino-victim.py
```

