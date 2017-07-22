import pygame
import player
import network

import control

class Game():
	def __init__(self):
		pygame.init()

		self.screen_size = [800, 600]
		self.screen = pygame.display.set_mode(self.screen_size)

		self.RUNNING, self.PAUSE = 0, 1
		self.state = self.RUNNING

		self.tick = 60

		self.id = None
		self.network_thread = None

		self.players = []

	def create_player(self, color, pos, id):
		p = player.Wizard(pygame, self.tick)
		p.pos = tuple(pos)
		p.color = color
		p.id = id
		p.load_texture()
		self.players.append(p)

	def main(self):
		pygame.display.set_caption("Wrestling of Magicians")

		done = False
		clock = pygame.time.Clock()

		p = player.Wizard(pygame, self.tick)
		self.players.append(p)

		n = network.Network(p, self)
		n.connect()

		for pl in self.players:
			pl.load_texture()
		#self.network_thread = threading.Thread(target=n.main)
		#self.network_thread.start()

		while not done:
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True

			if self.state == self.RUNNING:
				self.screen.fill((202,202,202))

				for pl in self.players:
					pl.draw(self.screen)
				dir = control.move_player(pygame)
				n.update({'move': dir})
			pygame.display.flip()
			clock.tick(self.tick)
		
		pygame.quit()

if __name__ == '__main__':
	g = Game()
	play = g.main()