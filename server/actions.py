move_speed = 2

def move_player(dir, clients, addr):
	for client in clients:
		if client['ip'] == addr[0] and client['port'] == addr[1]:
			if dir == 'up':
				client['pos'][1] -= move_speed
			elif dir == 'down':
				client['pos'][1] += move_speed
			elif dir == 'left':
				client['pos'][0] -= move_speed
			elif dir == 'right':
				client['pos'][0] += move_speed
			return clients, client
