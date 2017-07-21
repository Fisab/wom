def fabs(x):
	if x < 0:
		x *= -1
	return x

def change_color(surface, color, pygame):
	"""Fill all pixels of the surface with color, preserve transparency."""
	w, h = surface.get_size()
	r, g, b, _ = color
	except_col = [[255,255,235], [25,14,14], [255,212,168], [131,87,13]]
	for x in range(w):
		for y in range(h):
			a = surface.get_at((x, y))[3]
			old_col = list(surface.get_at((x,y)))
			change = True
			for col in except_col:
				for i in range(len(col)):
					if fabs(col[i] - old_col[i]) < 5:
						change = False
						break
			if change:
				surface.set_at((x, y), pygame.Color(r, g, b, a))