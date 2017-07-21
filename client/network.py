from socket import *
import sys

import time
#encode - перекодирует введенные данные в байты, decode - обратно

class Network():
	def __init__(self):
		self.host = 'localhost'
		self.port = 777

		self.id = None

		self.addr = (self.host, self.port)

		self.udp_socket = socket(AF_INET, SOCK_DGRAM)

	def connect(self):
		data = 's'#start
		data = str.encode(data)
		self.udp_socket.sendto(data, self.addr)

	def move_right(self):
		move_right_cmd = 'mr'#move_right
		data = str.encode(move_right_cmd, id)
		self.udp_socket.sendto(data, self.addr)

	def recv_data(self):
		data = self.udp_socket.recvfrom(1024)
		#data = bytes.decode(data)
		print(list(data))
		return data

	def disconnect(self):
		self.udp_socket.close()

	def main(self):
		self.connect()
		self.recv_data()

if __name__ == '__main__':
	while True:
		n = Network()
		n.main()
		time.sleep(1)
