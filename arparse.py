import argparse, socket, select, os, sys

parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("myIPhost")
parser.add_argument("yourIPhost")
args = parser.parse_args()
print('Chat started:', args.name, args.myIPhost, args.yourIPhost)

myName = args.name

myHostPort = args.myIPhost.split(':')
myHost = myHostPort[0]
myPort = int(myHostPort[1])

yourHostPort = args.yourIPhost.split(':')
yourHost = myHostPort[0]
yourPort = int(myHostPort[1])

# parsing complete time work with socket
