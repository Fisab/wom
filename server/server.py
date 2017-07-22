from socket import *
import json

from random import randint

import tools
import map

#
import threading

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

		self.timeout_time = 5#sec

		self.recv_thread = None
		self.recv_amount = 1024

		self.mult_pl_per_ip = True#multiple connect per 1 ip

	###	first connect
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
		pos = [randint(0, map_size[0]), randint(0, map_size[1])]
		r = {
			#system
			'ip': ip,
			'port': port,
			#advanced
			#'name': name,
			'color': color,
			'id': self.gen_id(),
			'pos': pos,
			'last_req': tools.get_time()
		}
		self.clients.append(r)
	def gen_start_msg(self, addr):
		client = self.get_client_via_addr(addr)
		res = {
			'color': palette[client['color']],
			'id': client['id'],
			'pos': client['pos']
		}
		r = json.dumps(res, separators=(',', ':'))
		r = str.encode(r)

		self.udp_socket.sendto(r, addr)
		
	def gen_data(self, addr):
		addr = list(addr)
		color = self.get_free_color()
		self.add_client(addr[0], addr[1], color)

	####

	def garbage_grabber(self):#delete timeout users
		cur_time = tools.get_time()
		for_delete = []
		for i in range(len(self.clients)):
			if cur_time - self.clients[i]['last_req'] > self.timeout_time:
				print('drop timeout - ', self.clients[i]['color'])
				for_delete.append(self.clients[i])
		for i in for_delete:
			self.clients.remove(i)

	def get_client_via_addr(self, addr):
		addr = list(addr)
		ip = addr[0]
		port = addr[1]
		for client in self.clients:
			if client['ip'] == ip and client['port'] == port:
				return client

	def check_already_connected(self, addr, port):
		for client in self.clients:
			if client['ip'] == addr and client['port'] == port:
				return True, False#connected? need drop?
			elif client['ip'] == addr:
				if self.mult_pl_per_ip:
					return True, False
				else:
					return True, True
		return False, False

	def recv(self):
		print(' - Server start recv data ', self.recv_amount, ' - ')
		while True:
			data, addr = self.udp_socket.recvfrom(self.recv_amount)
			print(data, addr)

			addr_ = list(addr)
			ip, port = addr_[0], addr_[1]
			connected, drop = self.check_already_connected(ip, port)
			if not drop:
				print(data.decode())
				self.gen_data(addr)
				self.gen_start_msg(addr)

	def main(self):
		print(' - Server will run on port %s - ' % self.port)
		while True:
			#self.recv()
			tools.sleep(self.timeout_time / 2)
			self.garbage_grabber()
			#print(len(self.clients))

if __name__ == '__main__':
	s = Server()
	s.recv_thread = threading.Thread(target=s.recv)
	s.recv_thread.start()
	s.main()