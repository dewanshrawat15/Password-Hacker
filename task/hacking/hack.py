# write your code here
import socket
import sys
import itertools


def generated_password(temp):
    letters = [str(i) for i in temp]
    newpassword = ''
    return temp


args = sys.argv
host = args[1]
port = int(args[2])
address = (host, port)

with socket.socket() as sock, open("passwords.txt") as src:
    sock.connect(address)
    for line in src:
        gen_pass = generated_password(line)
    sock.close()
