from socket import *
import sys

import time
import json
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

	def send(self, data):
		data = json.dumps(data, separators=(',', ':'))
		data = str.encode(data)

		self.udp_socket.sendto(data, self.addr)

	def connect(self):
		data = {'new': True}
		# data = 's'#start
		# data = str.encode(data)
		# self.udp_socket.sendto(data, self.addr)
		self.send(data)
		data = self.recv_data()
		self.set_settings(data[0])

	def update(self, msg):
		self.send(msg)
		data = self.recv_data()
		info = json.loads(data[0].decode())
		#print(info)
		updated_players_id = []
		#{'ur_hero': {'color': 'purple', 'pos': [346, 91], 'id': 2}, 'players': [{'color': [114, 163, 40], 'pos': [404, 156], 'id': 1}]}
		for player in self.client.players:
			if info['ur_hero']['id'] == player.get_id():
				player.set_pos(info['ur_hero']['pos'])
				updated_players_id.append(player.get_id())
			for player_ in info['players']:
				if player.get_id() == player_['id']:
					player.set_pos(player_['pos'])
					updated_players_id.append(player.get_id())
		#need_create = []
		for player_ in info['players']:
			if not player_['id'] in updated_players_id:
				self.client.create_player(player_['color'], player_['pos'], player_['id'])
				#need_create.append(player_['id'])

			#need_create.append()

	def set_settings(self, data):
		data = json.loads(data.decode())
		print(data)
		self.player.color = data['ur_hero']['color']
		self.player.pos = tuple(data['ur_hero']['pos'])
		self.client.id = data['id']
		self.player.id = data['id']
		#'players': [{'pos': [141, 115], 'color': [163, 134, 40]}]}
		for i in data['players']:
			self.client.create_player(i['color'], i['pos'], i['id'])

	def recv_data(self):
		ticker = 0
		#while True:
			#time.sleep(1)
		data = self.udp_socket.recvfrom(1024)
		return list(data)
		#print(list(data))

	def disconnect(self):
		self.udp_socket.close()

