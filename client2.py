import socket
import time
ip = '127.0.0.1'
port = 9999

c_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_soc.connect((ip, port))

while 1:
	
	msg = '/msg/h22';
	c_soc.sendall(msg.encode())
	data = c_soc.recv(128)
	msg = data.decode()
	print(msg)
	time.sleep(5)
