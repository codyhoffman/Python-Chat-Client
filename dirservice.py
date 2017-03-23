import sys, os, socket, struct, select, argparse


dirHost = '127.0.0.1'
dirPort = 7000
library = {}

dirserv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dirserv.bind((dirHost, dirPort))

dirserv.listen()


def decode_registration(msg_buf):
    tuple = struct.unpack('!HH16s16s', msg_buf[:36])
    (version, myName, UID, DID) = tuple
    myName = myName.decode('utf-8')
    UID = UID.decode('utf-8')
    DID = DID.decode('utf-8')
    return myName, UID, DID

def encode_response(errorCode, DID, version=150):
    header_buf = bytearray(36)
    errorCode = errorCode + ' ' * (16-len(errorCode))
    DID = DID + ' ' * (16-len(DID))

    header_buf = struct.pack('!HH16s16s', version, errorCode.encode('utf-8'), DID.encode('utf-8'))
    return header_buf

def findUser(yourName):
    if library.has_key(yourName):
        errorCode = '400'
        return library[yourName], errorCode
    else:
        errorCode = '600'
        return None, errorCode
try:

    while True:
        clientsocket, addr = dirserv.accept()
        print("Got a connection from %s" % str(addr))

        data = clientsocket.recv(4096)

        myName, UID, DID = decode_registration(data)

        library.update({myName: UID})

        yourIPHost, err = findUser(DID)

        clientsocket.send(encode_response(err, yourIPHost))
finally:
    print('TCP connection closed')
    clientsocket.close()


