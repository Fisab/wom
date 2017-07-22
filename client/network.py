from socket import *
import sys

import time
import json
import threading
#encode - перекодирует введенные данные в байты, decode - обратно

class Network():
	def __init__(self, player, client):
		self.host = 'localhost'
		self.port = 777

		self.id = None

		self.addr = (self.host, self.port)

		self.udp_socket = socket(AF_INET, SOCK_DGRAM)

		self.recv_thread = None

		self.ticker = 0

		self.player = player
		self.client = client

	def connect(self):
		data = 's'#start
		data = str.encode(data)
		self.udp_socket.sendto(data, self.addr)
		self.recv_data()

	def move_right(self):
		move_right_cmd = 'mr'#move_right
		data = str.encode(move_right_cmd, id)
		self.udp_socket.sendto(data, self.addr)

	def set_settings(self, data):
		data = json.loads(data.decode())
		print(data)
		self.player.color = data['color']
		self.player.pos = tuple(data['pos'])
		self.client.id = data['id']

	def recv_data(self):
		ticker = 0
		#while True:
			#time.sleep(1)
		data = self.udp_socket.recvfrom(1024)
		data = list(data)
		#print(list(data))
		self.set_settings(data[0])

	def disconnect(self):
		self.udp_socket.close()

	def main(self):
		self.connect()
		self.recv_data()

if __name__ == '__main__':
	n = Network()
	n.main()
