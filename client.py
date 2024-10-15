import socket

#client part of the process:
#second_step

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566 #we cna use any number larger than 1023 for port
ADDR = (IP, PORT)
SIZE = 100
FORMAT = "utf_8"
request_number = 10


def client():
    num_req = request_number
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect(ADDR) #the programe will puse here until the connection is accepted and established

        print(f"client connected to server server at {IP} : {PORT}")
        
        while True:

            for _ in range(num_req):
                MESSAGE = input()
            
                MESSAGE = MESSAGE + ".txt"
                s.send(MESSAGE.encode(FORMAT)) #client starts the process by sendeing data to the server
                MESSAGE = s.recv(SIZE).decode(FORMAT)
                print(f"[SERVER] {MESSAGE}")

client()



