import socket

ip_port = ('192.168.8.136', 13400)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ip_port)

while True:
    inp = input('<< type your message here: ').strip()
    if not inp:
        continue
    s.sendall(inp.encode())

    if inp == 'exit':
        print('>> disconnect, over and out')
        break

    server_reply = s.recv(1024).decode()
    print(server_reply)

s.close()