import socket
import threading
from connectionThread import connectionThread

class server:
    HOST = "89.163.145.12"
    PORT = 5802  
    print_lock = threading.Lock()
    online = True
    socket = None

    def __init__(self):
        try:
            self.init_server()
            self.connection_handling()
        except Exception as e:
            print(e)

    def init_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen(1024)
        print("Server started")

    def connection_handling(self):
        while self.online:
            client, address = self.socket.accept()
            self.print_lock.acquire()

            print('Connected to :', str(address[0]))
            connectionThread(client, address)

            self.print_lock.release()
        self.socket.close()
        print("Server Closed")

server()
