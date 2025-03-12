from scapy.all import sniff
import time, threading

buffer = {}
buffer_size = 0
session_started = "False"
startmac = ""
endmac   = ""
startbytes = "beefff" # By default
buffer["size"] = ""

def startmac_init(input):
	global startmac
	startmac = input

def endmac_init(input):
        global endmac
        endmac = input

def session_started_toggle():
	global session_started
	if session_started == "True":
		session_started = "False"
		#print("Changed sess to F")
	else:
		session_started = "True"
		#print("Changed sess to T")

def buffer_size_change(userin):
	global buffer_size
	buffer_size = userin

def decoder(message):
	message_bytes = bytes.fromhex(message)
	for byte in message_bytes:
		if byte < 32 or byte > 126:
			pass
		else:
			print(chr(byte), end='')

def display_message(frame):
	global session_started
	#global buffer_size
	global buffer
	if frame.haslayer("Dot11"):
		mac_payload = frame.addr2
		#print(frame.src)
		try:
			if mac_payload.lower().startswith(startbytes+":"):
				#print("Received info on session [+]")
				ctime = time.time()
				if session_started == "False" and str(mac_payload) != endmac:
					endmac_init("")
					#session_started_toggle()
					#print("Received info on session | size: " + )
					octet = str(mac_payload).split(":")[3] # get the 4th octet for chunk num
					octet_dec = int(octet, 16)      # get the size
					print("Received info on session | size: " + str(octet_dec) + " | " + str(mac_payload))
					#print(octet_dec)
					#buffer_size = dec         # set buffer size
					buffer["size"] = octet_dec
					#print(buffer)
					#session_started = True
					#session_started_toggle()
					#print(started_session)
					session_started_toggle()
					#print("debug")
					startmac_init(str(mac_payload))

				elif startmac != str(mac_payload) and endmac != str(mac_payload):
					print("Receiving byte stream: " + str(mac_payload) )
					chunk_num = str(mac_payload).split(":")[3] # get the 4th octet for chunk num
					chunk_num_dec = int(chunk_num, 16) # get the size
					byte1 = str(mac_payload).split(":")[4]
					byte2 = str(mac_payload).split(":")[5] 
					
					chunk = byte1 + byte2 #+ byte3 + byte4
					#delim = str(mac_payload)

					message_bytes = bytes.fromhex(chunk)
					chunk_d = ""
					for byte in message_bytes:
						if byte < 32 or byte > 126:
							pass
						else:
							#print(chr(byte), end="", flush=True)
							chunk_d += str(chr(byte))

					a = str(str(mac_payload).split(":")[3])
					buffer[chunk_num_dec] = chunk_d

					if buffer["size"] == chunk_num_dec and endmac != str(mac_payload):
						print(buffer)
						#session_started = False
						session_started_toggle()
						print("Chunk Transfer Complete.\n")
						#print(">> ")
						# display message
						result = ''.join(buffer[key] for key in sorted(k for k in buffer.keys() if k != "size" and isinstance(k, int)))
						print(result)

						startmac_init("")
						endmac_init(str(mac_payload))
						#buffer.clear() # clear buffer
		except Exception as e:
			pass

def start_collector():
	sniff(iface="wlp0s12f0mon", prn=display_message, store=0)

def main():
	sniff(iface="wlp0s12f0mon", prn=display_message, store=0)
	#thread = threading.Thread(target=start_collector)
	#thread.start()
	print(buffer)


if __name__ == "__main__":
	main()
