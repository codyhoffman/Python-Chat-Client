import sys, os, socket, struct, select, argparse


def encode_chat_msg(seqnum, UID, DID, msg, version=150):
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


msg = encode_chat_msg(3, 'abc', 'cdef', 'hello')
msg = decode_chat_msg(msg)[-1]
print(msg)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
count = 1

message = 'message variable'

sock.bind(server_address)

if count == 1:
    server_address = ('198.105.254.63', 10000)
    sock.bind(server_address)
    count += 1
try:
    while True:
        user_input = None
        print('>> ', end='', flush=True)
        rlist, wlist, elist = select.select([sock, sys.stdin], [], [])
        print('Select completed', rlist, wlist, elist)


        if sys.stdin in rlist:
            # if you do input when the sys.stdin has data available to read from,
            # it will NOT BLOCK
            user_input = input()

            print('sending "%s"' % user_input)
            user_input_bytes = user_input.encode('utf-8')
            sent = sock.sendto(user_input_bytes, server_address)

        if sock in rlist:
            # data is pending on the socket
            # reading form the socket will NOT block
            data, server = sock.recvfrom(4096)
            print('received "%s"' % msg)

finally:
    print('closing socket')
    sock.close()
