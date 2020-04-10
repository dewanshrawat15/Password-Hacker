# write your code here
import socket
import sys
import itertools

args = sys.argv
host = args[1]
port = int(args[2])
address = (host, port)

bits = [chr(x).lower() for x in range(65, 91)]
for i in range(10):
    bits.append(str(i))


def generate_password():
    for t in range(0, 32):
        for j in itertools.combinations_with_replacement(bits, t):
            yield j


def final_password(x):
    a = ''
    for letter in x:
        a = a + letter
    return a


def getpass(li):
    for x in range(1, len(li) + 1):
        for q in itertools.permutations(li, x):
            ans = final_password(q)
            yield ans


listOfPasswords = generate_password()
flag = 0
with socket.socket() as sock:
    sock.connect(address)
    while True:
        password = next(listOfPasswords)
        suitablePass = getpass(password)
        for i in suitablePass:
            generated_password = i.encode()
            sock.send(generated_password)
            resp = sock.recv(1024)
            response = resp.decode()
            if response == "Connection success!":
                flag = 1
                sock.close()
                break
        if flag == 1:
            break
    sock.close()

print(i)
