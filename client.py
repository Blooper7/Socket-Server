import socket
import sys

def run_client(server_ip, server_port, client_details=("127.0.0.1",40001)):
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client = socket.socket(("127.0.0.1",40001), socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind(client_details)
    client.connect((server_ip, server_port))
    
    #message loop
    while True:
        response = client.recv(1024)
        response = response.decode("utf-8")    
    
        print(f"Recieved: {response}")
        msg = input("Message: ")
        client.send(msg.encode("utf-8")[:1024])

        
        if response.lower() == "closed":
            break
        if msg == "/close":
            break
        
    client.close()
    print("Connection closed")

port=40001
if sys.argv[1] != None:
	port=int(sys.argv[1])
#run_client("127.0.0.1", 8000)
run_client("127.0.0.1", 8000, ("127.0.0.1", port))
#                              ^If not specified, defaulted to ("127.0.0.1", 40001)
