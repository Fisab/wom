from socket import *
import json

from random import randint

import tools
import map
import actions

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
		self.timeout = False

		self.recv_thread = None
		self.recv_amount = 1024

		self.mult_pl_per_ip = True#multiple connect per 1 ip

		self.max_id = 0

	###	first connect
	def gen_id(self):
		self.max_id += 1
		return self.max_id

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

	def get_all_players(self, id=None):
		#if id!=None return players without this
		res = []
		for client in self.clients:
			if id != None and client['id'] == id:
				continue
			res.append({
				'color': palette[client['color']],
				'pos': client['pos'],
				'id': client['id']
			})
		return res

	def gen_start_msg(self, addr):
		client = self.get_client_via_addr(addr)
		players = self.get_all_players()
		res = {
			'ur_hero': {
				'color': palette[client['color']],
				'pos': client['pos'],
				'id': client['id']
			},
			'id': client['id'],
			'players': players
		}
		self.send(addr, res)
		
	def gen_data(self, addr):
		addr = list(addr)
		color = self.get_free_color()
		self.add_client(addr[0], addr[1], color)

	####

	def send(self, addr, data):
		data = json.dumps(data, separators=(',', ':'))
		data = str.encode(data)
		#print(data)
		self.udp_socket.sendto(data, addr)

	def drop(self, addr):
		res = {'error': 'You already on server'}
		send(addr, data)
	#
	def garbage_grabber(self):#delete timeout users
		if not self.timeout:
			return
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

	def analyze_req(self, data, addr):
		data = json.loads(data.decode())
		if 'new' in data and data['new'] == True:
			self.gen_data(addr)
			self.gen_start_msg(addr)
		else:
			if 'move' in data:
				self.clients, cl = actions.move_player(data['move'], self.clients, addr)
				#{'last_req': 1500745798, 'pos': [267, 368], 'color': 'red', 'ip': '127.0.0.1', 'id': 1, 'port': 50263}
				r = {'ur_hero': {
									'pos': cl['pos'],
									'color': cl['color'],
									'id': cl['id']
								}, 
					 'players': self.get_all_players(cl['id'])}
				self.send(addr, r)



	def recv(self):
		print(' - Server start recv data ', self.recv_amount, ' - ')
		while True:
			data, addr = self.udp_socket.recvfrom(self.recv_amount)
			#print(data, addr)

			addr_ = list(addr)
			ip, port = addr_[0], addr_[1]
			connected, drop = self.check_already_connected(ip, port)
			
			if drop:
				self.drop(addr)
				continue
			self.analyze_req(data, addr)

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