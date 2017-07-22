def move_player(pygame):
	pressed = pygame.key.get_pressed()
	dir = ''

	if pressed[pygame.K_w]:
		dir = 'up'
	elif pressed[pygame.K_s]:
		dir = 'down'
	elif pressed[pygame.K_a]:
		dir = 'left'
	elif pressed[pygame.K_d]:
		dir = 'right'
	return dir
