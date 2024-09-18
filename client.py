import socket


def run_client(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client = socket.socket(("127.0.0.1",40001), socket.SOCK_STREAM)
    client.bind(("127.0.0.1",40001))
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
    
run_client("127.0.0.1", 8000)

