import sys, os, socket, struct, select, argparse


parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("myIPhost")
parser.add_argument("yourIPhost")
args = parser.parse_args()
print('Chat started:', args.name, args.myIPhost, args.yourIPhost)

myName = args.name
yourName = 'other user' # update this when directory service is implemented, as we have no idea what name is without directory

myHostPort = args.myIPhost.split(':')
myHost = myHostPort[0]
myPort = int(myHostPort[1])

yourHostPort = args.yourIPhost.split(':')
yourHost = yourHostPort[0]
yourPort = int(yourHostPort[1])
print('me:   ', myHost, myPort, 'you:  ', yourHost, yourPort)
seqnum = 1
# parsing complete time work with socket

#did = 'me' uid = (myHost, myPort) name = 'cody'
def encode_registration(myName, UID, DID, version=150):
    header_buf = bytearray(36)
    name = name + ' ' * (16-len(name))
    UID = UID + ' ' * (16-len(UID))
    DID = DID + ' ' * (16-len(UID))

    header_buf = struct.pack('!HH16s16s', version, name.encode('utf-8'), UID.encode('utf-8'), DID.encode('utf-8'))
    return header_buf


def encode_chat_msg(seqnum, UID, DID, msg, version=150):
    seqnum += 1
    header_buf = bytearray(36)
    UID = UID + ' ' * (16 - len(UID))
    DID = DID + ' ' * (16 - len(DID))

    header_buf = struct.pack('!HH16s16s', version, seqnum, UID.encode('utf-8'), DID.encode('utf-8'))
    header_buf = header_buf + msg.encode('utf-8')

    return header_buf


def decode_chat_msg(msg_buf):
    tuple = struct.unpack('!HH16s16s', msg_buf[:36])
    (version, seqnum, UID, DID) = tuple
    UID = UID.decode('utf-8')
    DID = DID.decode('utf-8')
    msg = msg_buf[36:].decode('utf-8')
    return (seqnum, UID, DID, msg)

# Open UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((myHost, myPort))

try:
    while True:
        user_input = None
        print(myName, '>> ', end='', flush=True)
        rlist, wlist, elist = select.select([sock, sys.stdin], [], [])
        #print('Select completed', rlist, wlist, elist)


        if sys.stdin in rlist:
            # if you do input when the sys.stdin has data available to read from,
            # it will NOT BLOCK
            user_input = input()

            #print('sending "%s"' % user_input)
            #user_input_bytes = user_input.encode('utf-8')
            user_input_bytes = encode_chat_msg(seqnum, 'ME', 'YOU', user_input)
            sent = sock.sendto(user_input_bytes, (yourHost, yourPort))
            #print('sent')

        if sock in rlist:
            # data is pending on the socket
            # reading form the socket will NOT block
            data, server = sock.recvfrom(4096)
            msg = decode_chat_msg(data)
            print('')
            print(yourName, '>> ', msg[3])

finally:
    print('closing socket')
    sock.close()
