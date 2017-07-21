from socket import *
import json

import time
from random import randint

import map

palette = {
	'brown': [163,134,40], 
	'green': [114,163,40],
	'blue': [51,156,163],
	'purple': [79,51,163],
	'red': [175,51,51],
	'pink': [239,49,246]
}
#udp_socket.close()

class Server():
	def __init__(self):
		self.host = '0.0.0.0'
		self.port = 777
		self.addr = (self.host, self.port)

		self.map = map.Map()

		self.udp_socket = socket(AF_INET, SOCK_DGRAM)
		self.udp_socket.bind(self.addr)

		self.clients = []

	def gen_id(self):
		return len(self.clients) + 1

	def get_free_color(self):
		busy_colors = []
		for client in self.clients:
			busy_colors.append(client['color'])
		for color in palette.keys():
			if not color in busy_colors:
				return color
		return list(palette.keys())[randint(0, len(palette.keys())-1)]

	def add_client(self, ip, port, color):
		map_size = self.map.get_size()
		pos = {
			'x': randint(0, map_size[0]),
			'y': randint(0, map_size[1])
		}
		r = {
			#system
			'ip': ip,
			'port': port,
			#advanced
			#'name': name,
			'color': color,
			'id': self.gen_id(),
			'pos': pos
		}
		self.clients.append(r)

	def get_client_via_addr(self, addr):
		addr = list(addr)
		ip = addr[0]
		port = addr[1]
		for client in self.clients:
			if client['ip'] == ip and client['port'] == port:
				return client

	def gen_data(self, addr):
		addr = list(addr)
		color = self.get_free_color()
		self.add_client(addr[0], addr[1], color)

	def gen_start_msg(self, addr):
		client = self.get_client_via_addr(addr)
		res = {
			'color': client['color'],
			'id': client['id'],
			'pos': client['pos']
		}
		r = json.dumps(res, separators=(',', ':'))
		r = str.encode(r)

		self.udp_socket.sendto(r, addr)

	def recv(self):
		data, addr = self.udp_socket.recvfrom(1024)
		print(data, addr)
		self.gen_data(addr)
		self.gen_start_msg(addr)

	def main(self):
		print(' - Server running on port %s - ' % self.port)
		while True:
			self.recv()

if __name__ == '__main__':
	s = Server()
	s.main()