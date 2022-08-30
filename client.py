#!/usr/bin/env python

# Author: Rodney Boyce

from PyQt5 import QtWidgets, QtCore, QtGui

import socket
import pickle
import sys
from tcp import *

class LoginWindow(QtWidgets.QMainWindow):
    switchWindows = QtCore.pyqtSignal()

    def __init__(self, client, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.client = client
        self.setupUI()

    def setupUI(self):
        self.setObjectName("MainWindow")
        self.resize(1253, 703)
        self.setStyleSheet("background-color: rgb(170, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.mainTitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainTitleLabel.setGeometry(QtCore.QRect(10, 10, 1231, 461))
        font = QtGui.QFont()
        font.setFamily("Showcard Gothic")
        font.setPointSize(90)
        self.mainTitleLabel.setFont(font)
        self.mainTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainTitleLabel.setObjectName("mainTitleLabel")

        self.usernameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.usernameInput.setGeometry(QtCore.QRect(350, 530, 271, 41))
        self.usernameInput.setObjectName("usernameInput")

        self.passwordInput = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordInput.setGeometry(QtCore.QRect(640, 530, 271, 41))
        self.passwordInput.setObjectName("passwordInput")

        self.loginButton = QtWidgets.QPushButton(self.centralwidget)
        self.loginButton.setGeometry(QtCore.QRect(350, 580, 561, 71))
        font = QtGui.QFont()
        font.setFamily("Showcard Gothic")
        font.setPointSize(20)

        self.loginButton.setFont(font)
        self.loginButton.setStyleSheet("border-color: rgb(0, 0, 0);\n"
"border-width : 3px;\n"
"border-style:solid;")
        self.loginButton.setObjectName("loginButton")
        self.loginButton.clicked.connect(self.login)

        self.usernameLabel = QtWidgets.QLabel(self.centralwidget)
        self.usernameLabel.setGeometry(QtCore.QRect(350, 490, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Showcard Gothic")
        font.setPointSize(20)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.usernameLabel.setObjectName("usernameLabel")

        self.passwordLabel = QtWidgets.QLabel(self.centralwidget)
        self.passwordLabel.setGeometry(QtCore.QRect(640, 490, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Showcard Gothic")
        font.setPointSize(20)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.passwordLabel.setObjectName("passwordLabel")

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
        self.mainTitleLabel.setText(_translate("MainWindow", "Rod\'s IRC"))
        self.loginButton.setText(_translate("MainWindow", "LOGIN"))
        self.usernameLabel.setText(_translate("MainWindow", "Username"))
        self.passwordLabel.setText(_translate("MainWindow", "Password"))

    def login(self):
        given_username = self.usernameInput.text()
        given_password = self.passwordInput.text()
        loginStatus = self.client.login(given_username, given_password)
        if loginStatus == "VALID LOGIN":
            self.client.start()
            self.switchWindows.emit()
        elif loginStatus == "INVALID USERNAME":
            # TODO Create popup windows for these errors
            pass
        elif loginStatus == "INVALID PASSWORD":
            # TODO Create popup windows for these errors
            pass
        elif loginStatus == "EXISTING":
            # TODO Create popup windows for these errors
            pass

class MessageWindow(QtWidgets.QMainWindow):
    def __init__(self, client, parent=None):
        super(MessageWindow, self).__init__(parent)
        self.client = client
        self.client.updateMessage.connect(self.displayMessage)
        self.client.addUserToList.connect(self.addUserToList)
        self.client.removeUserFromList.connect(self.removeUserFromList)
        self.client.populateUserList.connect(self.populateUserList)
        self.setupUI()

    def setupUI(self):
        self.setObjectName("MainWindow")
        self.resize(1253, 703)
        self.setStyleSheet("background-color: rgb(170, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(850, 600, 101, 71))
        self.pushButton.setStyleSheet("background-color: rgb(170, 0, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"border-width : 3px;\n"
"border-style:solid;\n"
"font: 81 20pt \"Rockwell Extra Bold\";")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)

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
        self.messageWindow.setFocusPolicy(QtCore.Qt.NoFocus)

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
        self.userList.setFocusPolicy(QtCore.Qt.NoFocus)

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
        if data != "":
            self.messageInput.clear()
            TCP_Send(self.client.socket, "MESSAGE".encode())
            TCP_Send(self.client.socket, data.encode())

    def displayMessage(self, message):
        self.messageWindow.append(message)

    def copyUser(self):
        user = self.userList.selectedItems()[0]
        QtWidgets.QApplication.clipboard().setText(user.text())

    def removeUserFromList(self, user):
        item = self.userList.findItems(user, QtCore.Qt.MatchExactly)[0]
        self.userList.takeItem(self.userList.row(item))

    def addUserToList(self, user):
        self.userList.addItem(user)
        self.userList.sortItems()

    def populateUserList(self, userList):
        self.userList.clear()
        self.userList.addItems(userList)
        self.userList.sortItems()

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
        userList = pickle.loads(TCP_Recv(self.socket))
        self.populateUserList.emit(userList)
        while self.state:
            try:
                self.__listen()
            except:
                print("Server has shutdown. Bye!")
                sys.exit()

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

    def login(self, u, p):
        TCP_Send(self.socket, u.encode())
        TCP_Send(self.socket, p.encode())
        return TCP_Recv(self.socket).decode()
    

    def closeClient(self):
        TCP_Send(self.socket, "EXIT".encode())
        self.state = False

class MainWindow(QtWidgets.QStackedWidget):
    def __init__(self, client, parent = None):
        super(MainWindow, self).__init__(parent)
        self.client = client
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.client.closeClient()
        return super().closeEvent(a0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    client = TCP_Client()
    widgetStack = MainWindow(client)
    loginWindow = LoginWindow(client)
    messageWindow = MessageWindow(client)
    widgetStack.addWidget(loginWindow)
    widgetStack.addWidget(messageWindow)
    loginWindow.switchWindows.connect(lambda: widgetStack.setCurrentIndex(1))

    widgetStack.setFixedSize(1253, 703)
    widgetStack.show()

    sys.exit(app.exec_())