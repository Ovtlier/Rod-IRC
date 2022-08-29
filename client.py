#!/usr/bin/env python

# Author: Rodney Boyce

from PyQt5 import QtWidgets, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import socket
import pickle
import sys
from tcp import *

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.client = TCP_Client()
        self.client.updateMessage.connect(self.displayMessage)
        self.client.addUserToList.connect(self.addUserToList)
        self.client.removeUserFromList.connect(self.removeUserFromList)
        self.client.populateUserList.connect(self.populateUserList)
        self.client.start()
        
        self.setObjectName("MainWindow")
        self.setFixedSize(1253, 703)
        self.setStyleSheet("background-color: rgb(170, 0, 0);")

    def setupUi(self):
        
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(850, 600, 101, 71))
        self.pushButton.setStyleSheet("background-color: rgb(170, 0, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"border-width : 3px;\n"
"border-style:solid;\n"
"font: 81 20pt \"Rockwell Extra Bold\";")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setFocusPolicy(Qt.NoFocus)

        self.messageWindow = QtWidgets.QTextEdit(self.centralwidget)
        self.messageWindow.setGeometry(QtCore.QRect(20, 60, 931, 531))
        self.messageWindow.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"border-width : 3px;\n"
"border-style:solid;\n"
"font: 75 16pt \"Arial\";\n"
"color:rgb(255, 255, 255);")
        self.messageWindow.setObjectName("messageWindow")
        self.messageWindow.setReadOnly(True)
        self.messageWindow.setFocusPolicy(Qt.NoFocus)

        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(20, 10, 931, 41))
        self.titleLabel.setStyleSheet("background-color: rgb(170, 0, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"border-width : 3px;\n"
"border-style:solid;\n"
"font: 81 20pt \"Rockwell Extra Bold\";\n"
"")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(960, -20, 281, 711))
        self.frame.setStyleSheet("background-color:rgb(170, 0, 0)")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.userList = QtWidgets.QListWidget(self.frame)
        self.userList.setGeometry(QtCore.QRect(10, 80, 261, 611))
        self.userList.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"border-width : 3px;\n"
"border-style:solid;\n"
"font: 75 16pt \"Arial\";\n"
"color:rgb(255, 255, 255);")
        self.userList.setObjectName("userList")
        self.userList.itemClicked.connect(self.copyUser)
        self.userList.setFocusPolicy(Qt.NoFocus)

        self.userListLabel = QtWidgets.QLabel(self.frame)
        self.userListLabel.setGeometry(QtCore.QRect(10, 30, 261, 41))
        self.userListLabel.setStyleSheet("background-color:rgb(170, 0, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"border-width : 3px;\n"
"border-style:solid;\n"
"font: 81 20pt \"Rockwell Extra Bold\";")
        self.userListLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.userListLabel.setObjectName("userListLabel")

        self.messageInput = QtWidgets.QTextEdit(self.centralwidget)
        self.messageInput.setGeometry(QtCore.QRect(20, 600, 821, 71))
        self.messageInput.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"border-width : 3px;\n"
"border-style:solid;\n"
"font: 75 16pt \"Arial\";\n"
"color:rgb(255, 255, 255);")
        self.messageInput.setObjectName("messageInput")
        self.messageInput.setFocus()
        self.messageInput.installEventFilter(self)

        self.pushButton.clicked.connect(self.sendMessage)

        self.frame.raise_()
        self.pushButton.raise_()
        self.messageWindow.raise_()
        self.titleLabel.raise_()
        self.messageInput.raise_()

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1253, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "SEND"))
        self.titleLabel.setText(_translate("MainWindow", "Rod\'s Messaging Service"))
        self.userListLabel.setText(_translate("MainWindow", "Active Users"))

    def sendMessage(self):
        data = self.messageInput.toPlainText()
        self.messageInput.clear()
        TCP_Send(self.client.socket, "MESSAGE".encode())
        TCP_Send(self.client.socket, data.encode())

    def displayMessage(self, message):
        self.messageWindow.append(message)

    def copyUser(self):
        user = self.userList.selectedItems()[0]
        QApplication.clipboard().setText(user.text())

    def removeUserFromList(self, user):
        item = self.userList.findItems(user, QtCore.Qt.MatchExactly)[0]
        self.userList.takeItem(self.userList.row(item))

    def addUserToList(self, user):
        self.userList.addItem(user)
        self.userList.sortItems()

    def populateUserList(self, userList):
        sys.stdout.flush()
        for user in userList:
            self.userList.addItem(user["username"])
        self.userList.sortItems()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.client.closeClient()
        return super().closeEvent(a0)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.messageInput:
            if event.key() == QtCore.Qt.Key_Return and self.messageInput.hasFocus():
                self.sendMessage()
                return True
        return super().eventFilter(obj, event)

class TCP_Client(QtCore.QThread):

    updateMessage = QtCore.pyqtSignal(object)
    addUserToList = QtCore.pyqtSignal(object)
    removeUserFromList = QtCore.pyqtSignal(object)
    populateUserList = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.daemon = True
        self.state = True

        self.server_host = "192.168.8.103"
        self.server_port = 9999

        try:
            self.server_address = (self.server_host, self.server_port)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.server_address)
        except:
            print("Server is not online.")
            sys.exit()
    
    def run(self):
        self.__login()
        userList = pickle.loads(TCP_Recv(self.socket))
        self.populateUserList.emit(userList)
        while self.state:
            self.__listen()

    def __listen(self):
        data = TCP_Recv(self.socket).decode()
        if data == "ACTIVE USER":
            data = TCP_Recv(self.socket).decode()
            if data == "ADD":
                data = TCP_Recv(self.socket).decode()
                self.addUserToList.emit(data)
            elif data == "REMOVE":
                data = TCP_Recv(self.socket).decode()
                self.removeUserFromList.emit(data)
        elif data == "MESSAGE":
            data = TCP_Recv(self.socket).decode()
            self.updateMessage.emit(data)

    def __login(self):
        # LOGIN
        # Username
        username = input("Username: ")
        TCP_Send(self.socket, username.encode())
        data = TCP_Recv(self.socket).decode()
        while data == "INVALID":
            print("Invalid Username. Please try again")
            username = input("Username: ")
            TCP_Send(self.socket, username.encode())
            data = TCP_Recv(self.socket).decode()
            
        # Password
        logged_in = False
        while not logged_in:
            password = input("Password: ")
            TCP_Send(self.socket, password.encode())
            data = TCP_Recv(self.socket).decode()
            if data == "VALID":
                logged_in = True
            else:
                print("Invalid Password. Please try again")

    def closeClient(self):
        TCP_Send(self.socket, "EXIT".encode())
        self.state = False

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = Ui_MainWindow()
    gui.setupUi()
    gui.show()

    sys.exit(app.exec_())


'''
            TCP_Send(self.client_socket, message.encode())

            # receive response from the server
            # 1024 is a suggested packet size, you can specify it as 2048 or others
            data = TCP_Recv(self.client_socket)
            received_message = data.decode()

            # parse the message received from server and take corresponding actions
            if received_message == "":
                print("[recv] Message from server is empty!")
            elif received_message == "logout":
                message = self.username
                TCP_Send(self.client_socket, message.encode())
                message = TCP_Recv(self.client_socket).decode()
                print(message)
                print(f"Bye, {self.username}!")
                break
            elif received_message == "Broadcast message":
                message = self.username
                TCP_Send(self.client_socket, message.encode())
                message = TCP_Recv(self.client_socket).decode()
                print(message)
            elif received_message == "Active users":
                message = self.username
                TCP_Send(self.client_socket, message.encode())
                num_users = int(TCP_Recv(self.client_socket).decode())
                if num_users != 0:
                    for i in range(0, num_users):
                        a_user = TCP_Recv(self.client_socket).decode()
                        print(a_user)
                else:
                    error = TCP_Recv(self.client_socket).decode()
                    print(error)
'''