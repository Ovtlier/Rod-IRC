#!/usr/bin/env python

# Author: Rodney Boyce

from datetime import datetime, timedelta
from tcp import TCP_Recv, TCP_Send

import sys
import socket
import threading
import pickle

curr_active_users = []                  # List for now?
private_rooms = []
valid_accounts = {}
clients = {}

with open("credentials.txt", "r") as f:
    creds = f.readlines()
    creds = [line.rstrip() for line in creds]
    for user in creds:
        username, password = user.split()
        valid_accounts[username] = valid_accounts.get(username, password)
print(valid_accounts)

class ClientThread(threading.Thread):
    def __init__(self, address, socket):
        threading.Thread.__init__(self)
        self.username = None
        self.address = address
        self.socket = socket
        self.__login()
        clients[self.username] = clients.get(self.username, socket)
        self.state = True
        self.__sendActiveUsers()
        self.__updateOtherUsers("ADD")
        print("New client thread made!")

    def run(self):
        while self.state:
            self.__listen()
        print("Client loop has ended")
        self.socket.close()
        sys.stdout.flush()

    def __login(self):
        data = TCP_Recv(self.socket)
        self.username = data.decode()
        while self.username not in valid_accounts:
            data = "INVALID"
            TCP_Send(self.socket, data.encode())
            data = TCP_Recv(self.socket)
            self.username = data.decode()
        logged_in = False
        data = "VALID"
        TCP_Send(self.socket, data.encode())
        
        while not logged_in:
            data = TCP_Recv(self.socket)
            password = data.decode()
            print(f"CHECK {password} == {valid_accounts[self.username]}")
            is_correct_password = password == valid_accounts[self.username]
            if is_correct_password:
                data = "VALID"
                TCP_Send(self.socket, data.encode())
                log_timestamp = datetime.now().strftime("%d %b %Y %H:%M:%S")
                a_user = {}
                a_user["username"] = self.username
                a_user["ip"] = self.address[0]
                a_user["login_time"] = log_timestamp
                curr_active_users.append(a_user)
                log_num = len(curr_active_users)
                with open("userlog.txt", "a") as user_log:
                    user_log.write(f"{log_num}; {log_timestamp}; {username}; {self.address}\n")
                logged_in = True
                print("User {} has connected from {}.".format(self.username, self.address))
            else:
                message = "INVALID"
                TCP_Send(self.socket, message.encode())

    def __listen(self):
        data = TCP_Recv(self.socket).decode()
        if data == None or data == "EXIT":
            print("{} from {} has exited.".format(self.username, self.address))
            self.__updateOtherUsers("REMOVE")
            self.state = False
        elif data == "MESSAGE":
            data = TCP_Recv(self.socket).decode()
            log_num = sum(1 for line in open("messagelog.txt")) + 1
            log_timestamp = datetime.now().strftime("%d %b %Y %H:%M:%S")
            log_data = f"{log_num}; {log_timestamp}; {self.username}; {data}"
            self.__write_to_log("messagelog.txt", log_data)
            prettyMessage = f"({log_timestamp}) {self.username}: {data}"
            self.__speak(prettyMessage)
            print(log_data)

    def __speak(self, data):
        for c in clients:
            prefix = "MESSAGE"
            TCP_Send(clients[c], prefix.encode())
            TCP_Send(clients[c], data.encode())

    def __updateOtherUsers(self, prefix):
        if prefix == "REMOVE":
            del clients[self.username]

        for c in clients:
            if c != self.username:
                TCP_Send(clients[c], "ACTIVE USER".encode())
                TCP_Send(clients[c], prefix.encode())
                TCP_Send(clients[c], self.username.encode())

    def __write_to_log(self, log_name, data):
        with open(log_name, "a") as f:
            f.write(data + "\n")

    def __sendActiveUsers(self):
        TCP_Send(self.socket, pickle.dumps(curr_active_users))

if __name__ == "__main__":
    # Error checking given args
    if len(sys.argv) != 2:
        print("Usage: python3 server.py server_port")
        exit(0)

    try:
        server_port = int(sys.argv[1])
    except:
        print("Error: invalid port number!")
        exit(0)
    
    # Setting up server socket
    server_address = ("", server_port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)

    # Creating log files??? Are they needed?
    temp = open("messagelog.txt", "w")
    temp.close()

    print("Server started on [" + socket.gethostbyname(socket.gethostname()) + ", " + str(server_port) + "]")

    while True:
        server_socket.listen()
        client_socket, client_address = server_socket.accept()
        client_thread = ClientThread(client_address, client_socket)
        client_thread.start()