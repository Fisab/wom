import pygame
import player

class Game():
	def __init__(self):
		pygame.init()

		self.screen_size = [800, 600]
		self.screen = pygame.display.set_mode(self.screen_size)

		self.RUNNING, self.PAUSE = 0, 1
		self.state = self.RUNNING

		self.tick = 60

	def main(self):
		pygame.display.set_caption("Wrestling of magicians")

		done = False
		clock = pygame.time.Clock()

		p = player.Wizard(pygame, self.tick)

		while not done:
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True

			if self.state == self.RUNNING:
				self.screen.fill((202,202,202))

				p.draw(self.screen)

			pygame.display.flip()
			clock.tick(self.tick)
		
		pygame.quit()

if __name__ == '__main__':
	g = Game()
	play = g.main()