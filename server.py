import socket
import threading
import random

#https://www.datacamp.com/tutorial/a-complete-guide-to-socket-programming-in-python

server_ip = "127.0.0.1"
port = 8000

callsigns={}

def generateCallsign():
	alpha="BCDFGHJKLMNPQRSTVWXZ"
	callsign=""
	for i in range(4):
		callsign+=alpha[random.randint(0, len(alpha)-1)]
	return callsign

def handle_client(client_socket, addr):
	try:
		client_socket.send(f"ASSIGNED CALLSIGN: {callsigns[addr]}".encode("utf-8"))
		while True:
			request = client_socket.recv(1024).decode("utf-8")
			if request.lower() == "/close":
				client_socket.send("closed".encode("utf-8"))
				break
			print(f"{callsigns[addr]}: {request}")
			response = "accepted"
			client_socket.send(response.encode("utf-8"))
	except Exception as e:
		print(f"Client handling error: {e}")
	finally:
		client_socket.close()
		print(f"Closed connection to {addr[0]}:{addr[1]}")

def start_server(ip, prt):
    try:
    	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    	server.bind((ip,prt))
    	server.listen()
    	print(f"Listening on {ip}:{prt}")
    
    	while True:
    		client_socket, addr = server.accept()
    		print(f"Connection accepted from {addr[0]}:{addr[1]}")
    		
    		newCallsign=generateCallsign()
    		while newCallsign in callsigns:
    			newCallsign=generateCallsign()
    		
    		callsigns[addr]=newCallsign
    		
    		thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
    		thread.start()
    except Exception as e:
    	print(f"Error: {e}")
    	server.close()
    	
start_server(server_ip, port)
