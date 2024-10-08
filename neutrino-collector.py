from scapy.all import sniff
import time, threading

buffer = {}

def decoder(message):
	message_bytes = bytes.fromhex(message)
	for byte in message_bytes:
		if byte < 32 or byte > 126:
			pass
		else:
			print(chr(byte), end='')

def display_message(frame):
	if frame.haslayer("Dot11"):
		mac_payload = frame.addr2
		#print(frame.src)
		try:
			if mac_payload.lower().startswith("aa:"):
				ctime = time.time()
				if mac_payload not in buffer or ctime - buffer[mac_payload] > 5:
					#print(str(mac_payload))
					# Now print ascii value
					delim = str(mac_payload)
					delim2 = delim.replace(":","")
					#delim3 = delim2.replace("00","")

					message_bytes = bytes.fromhex(delim2)
					for byte in message_bytes:
                				if byte < 32 or byte > 126:
                        				pass
                				else:
                        				print(chr(byte), end="", flush=True)
					#delim2 = delim.replace("00","")
					#ascii_val = bytes.fromhex(delim2).decode('ascii')
					#print(f"{repr(str(delim2).decode('ascii', errors='replace'))}") #print(str(ascii_val))
					#thread = threading.Thread(target=decoder(delim2))
					#thread.start()
					#thread.join()
					buffer[mac_payload] = ctime
				#time.sleep(2)
		except Exception as e:
			pass
sniff(iface="wlp0s12f0mon", prn=display_message, store=0)
