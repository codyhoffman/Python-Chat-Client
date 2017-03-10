import sys, os, socket, struct, select, argparse


name = 'test'
IpHost = '127.0.0.1:7000'


def encode_chat_msg(seqnum, UID, DID, msg, version=150):
    seqnum += 1
    header_buf = bytearray(36)
    UID = UID + ' ' * (16 - len(UID))
    DID = DID + ' ' * (16 - len(DID))

    header_buf = struct.pack('!HH16s16s', version, seqnum, UID.encode('utf-8'), DID.encode('utf-8'))
    header_buf = header_buf + msg.encode('utf-8')

    return header_buf

library = {"cody": '127.0.0.1:5000', 'sam': '127.0.0.1:6000'}

library.update({name: IpHost})

print(library)
