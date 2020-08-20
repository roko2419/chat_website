from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock


class Client:
    # constants set when Client is called
    HOST = "localhost"
    PORT = 5600
    ADDR = (HOST, PORT)
    BUFSIZ = 512
    run = True

    def __init__(self, name):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.name = name
        self.messages = []
        receive_thread = Thread(target=self.receive_message)
        receive_thread.start()
        # send first message as name___
        self.send_messages(name)
        self.lock = Lock()

    def send_messages(self, msg):
        self.client_socket.send(msg.encode("utf8"))
        if msg == "{quit}":
            self.run = False
            self.client_socket.close()

    def receive_message(self):
        # ----- needs fixing ------
        # ------ problem: infinite loop
        # connection is terminated from server side but thread will still be running-----
        # ------ solution: if send(msg) == {quit}  exit loop  -----
        while self.run:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.lock.acquire()
                self.messages.append(msg)
                # print(f"({self.name})->>{msg}")
                self.lock.release()
            except Exception as e:
                # print("[EXCEPTION]", e)
                break

    def get_messages(self):
        # creates a copy of messages list
        messages_copy = self.messages[:]
        # to saving space
        # self.lock.acquire()
        # self.messages = []
        # self.lock.release()
        # returns: the copy of messages
        return messages_copy

    def disconnect(self):
        self.messages = []
        self.send_messages("{quit}")
        self.client_socket.close()
