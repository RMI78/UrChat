import threading
import socket

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.clients = []

        self.main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_connection.bind((self.host, self.port))
    
    def run(self):

        while True:
            self.wait_connection()


    def wait_connection(self):
        """
        Wait and init a connection
        :param:
        :return:
        """
        self.main_connection.listen()
        conn, addr = self.main_connection.accept()
        self.clients.append({"ip":str(addr), 
                             "conn":conn, 
                             "thread" : threading.Thread(target=self.propagate_msg, args=(conn,))})
        self.clients[-1]["thread"].start()



    def send_message(self, login, message):
        """
        Send message to client
        :param client, message:
        :return:
        """
        self.clients[login]["con"].send(message)

    def commands_read(self, text, client):
        if len(text) == 0:
            return True
        elif "!exit" in str(text)[2:-1]:
            client.send("goodbye")
            return False
        else:
            return True


    def propagate_msg(self, client_conn):
        msg=""
        while self.commands_read(msg, client_conn):
            msg = client_conn.recv(1024)
            for c in self.clients:
                c["conn"].send(msg)
        toRemove = None
        for c in self.clients:
            if c["conn"] == client_conn:
                toRemove = c
                break
        self.clients.remove(toRemove)

