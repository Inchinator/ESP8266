from threading import *

class connectionThread (Thread):

    def __init__(self, client, address):
        super(connectionThread, self).__init__()
        self.reply = "ping reply".encode("ascii")
        self.client = client
        self.address = address
        self.start()

    def run(self):
        try:
            # print("client: " + str(self.client)) # socketInfo
            # print("address: " + str(self.address)) # Connection-info

            received_data = self.client.recv(1024).decode('ascii')

            if (received_data == "ping"):
                self.client.send(self.reply)
            else:
                self.client.send("-".encode("ascii"))

        except Exception as e:
            print(e)

        finally:
            self.client.close()
