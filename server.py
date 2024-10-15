import socket
from queue import Queue
import signal
import threading

from concurrent.futures import ThreadPoolExecutor #-> creat a thread pool and execute some code
# concurrent -> high level vertion of threading  
# future -> we are going work with the value but we dont know what that value is. we are going to get that value in the future. 


#server part of the process:

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566 #we cna use any number larger than 1023 for port
ADDR = (IP, PORT)
SIZE = 100
FORMAT = "utf_8"
DISCONNECT_MESSAGE = "DISCONNECT"
VALID = ["test1.txt", "test2.txt", "test3.txt"]
    
number_of_threds = 5
executor = ThreadPoolExecutor(number_of_threds)

request_number = 10


def worker(MESSAGE):
    if (len(MESSAGE) > 10): #invalid request
        return "invalid request, 400 error"
    else:
        T = True
        for i in range(3):
            if MESSAGE == VALID[i]:
                T = False
                file = open(f"{MESSAGE}","r")
                response = file.read()
                return response
                break 
        if T == True:
            return "the file does not exist, 404 error"
        

def shared_queue(request, queue, conn, addr):
    queue.put(request)
    future = executor.submit(worker, queue.get())
    print(f"[{addr}] {request}")
    MESSAGE = f"your message is: {request} \n our response is: {future.result()}"
    conn.send(MESSAGE.encode(FORMAT))



def signal_handler(signum, frame):

    print("SIGINT received. all threads are terminating...")
    executor.shutdown(wait=False)
    socket.close

    print("Server Closed.")




def server():
    print("server is starting...")
    queue = Queue()
    num_req = request_number 

    # first_step server sets up a listening socket
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:# this creats a listening socket
        s.bind(ADDR)
        s.listen() #this going to isten for a request to the server from the socket
        print(f"server is listening on {IP} : {PORT}")

        signal.signal(signal.SIGINT, signal_handler)

        num = number_of_threds + 1

        while True:
            conn , addr = s.accept() #blocking-> the programe will puse waiting to accept the connection  
            #conn->new socket 
            #addr->the port that new socket will use
            
            for _ in range(num_req):
                MESSAGE = conn.recv(SIZE).decode(FORMAT)
                
                num -= 1
                if num == 0:
                    MESSAGE = f"your request ({MESSAGE}) is rejected, 503 error"
                    conn.send(MESSAGE.encode(FORMAT))
                    break

                else:
                    shared_queue(MESSAGE, queue, conn, addr)
                    

            conn.close()
    


server()