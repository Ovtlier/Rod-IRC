# Author: Rodney Boyce

import socket
import struct

def TCP_Send(socket, data):
    socket.sendall(struct.pack("!I", len(data)))
    socket.sendall(data)

def __TCP_Recvall(socket, size):
    data = b""
    while size:
        temp = socket.recv(size)
        if not temp:
            return None
        data += temp
        size -= len(temp)
    return data

def TCP_Recv(socket):
    size = __TCP_Recvall(socket, 4)
    if size == None:
        return b""
    return __TCP_Recvall(socket, struct.unpack("!I", size)[0])
    
