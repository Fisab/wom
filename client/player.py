import tools

class Wizard():
	def __init__(self, pygame, tick):
		self.pygame = pygame

		self.pos = None

		#textures
		self.hero_size = (40, 40)
		self.color = None

		self.cur_rect_pos = (20, 15, 18, 19)#8x6
		#self.load_texture()

		self.tick = tick

		self.counter = 0

		self.id = None

		self.MOVE, self.STAY = 0, 1

		self.state = self.STAY

		self.stay_rect_poses = {'pos': [(20, 15, 18, 19), (62, 15, 18, 19)], 'interval': 1.25}
		self.move_rect_poses = {'pos': [(20, 15, 18, 19), (40, 15, 18, 19), (60, 15, 18, 19), (80, 15, 18, 19)], 'interval': 4}

	def get_id(self):
		return self.id

	def load_texture(self):
		self.image = self.pygame.image.load("data/heroes/wizard_standart.png")

		tools.change_color(self.image, self.pygame.Color(*self.color), self.pygame)
		self.img_draw = self.image.subsurface(self.cur_rect_pos)
		self.img_draw = self.pygame.transform.scale(self.img_draw, self.hero_size)

	def change_rect(self):
		self.img_draw = self.image.subsurface(self.cur_rect_pos)
		self.img_draw = self.pygame.transform.scale(self.img_draw, self.hero_size)

	def set_pos(self, new_pos):
		if self.pos == new_pos:
			self.state = self.STAY
		else:
			self.state = self.MOVE
		self.pos = tuple(new_pos)

	def animate_sprite(self):
		if self.state == self.MOVE:
			arr_rect = self.move_rect_poses['pos']
			interval = self.move_rect_poses['interval']
		elif self.state == self.STAY:
			arr_rect = self.stay_rect_poses['pos']
			interval = self.stay_rect_poses['interval']

		if self.counter == self.tick / interval:
			if not self.cur_rect_pos in arr_rect:
				index = 0
			else:
				index = arr_rect.index(self.cur_rect_pos)
			if index + 1 == len(arr_rect):
				index = 0
			else:
				index += 1

			self.cur_rect_pos = arr_rect[index]
			self.change_rect()

			self.counter = 0

		self.counter += 1
	
	def draw(self, screen):
		#pass
		#print(self.pos)
		screen.blit(self.img_draw, self.pos)
		self.animate_sprite()
			
