import pygame,sys,time
from vector3 import Vector3
from fireworks import *
from random import randint
from force_generator import *

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 400
PIXELS_PER_METER = 100

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fireworks")
font = pygame.font.SysFont("Ubuntu",20)
active_fireworks = []

forces = ParticleForceRegistry()
gravity = ParticleGravity(Vector3(0,15,0))
drag = ParticleDrag(0.1,0.01)

def world_to_screen(pos):
    return (pos[0] * PIXELS_PER_METER, pos[1] * PIXELS_PER_METER)

def screen_to_world(pos):
    return (pos[0] / PIXELS_PER_METER, pos[1] / PIXELS_PER_METER)

previous_time = time.time()
while True:
	dt = time.time() - previous_time
	previous_time = time.time()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				pos = screen_to_world(pygame.mouse.get_pos())
				firework = rules[0].create_firework(Vector3(*pos,0))
				active_fireworks.append(firework)

	screen.fill((100,100,100))
	
	# Draw
	text = font.render(f"{(1/dt):.2f}","black",False)
	screen.blit(text,(0,0))

	forces.clear()
	for firework in active_fireworks[:]:
		forces.add(firework,gravity)
		# forces.add(firework,drag)
		firework.age -= 0.1
		pos = world_to_screen((firework.position.x,firework.position.y))
		# print(pos)
		pygame.draw.circle(screen,"white",pos,firework.radius)

		if firework.age <= 0:
			new_fireworks = explode_firework(firework,rules)
			active_fireworks.remove(firework)
			active_fireworks.extend(new_fireworks)

	forces.update_forces()

	for firework in active_fireworks:
		firework.update(dt)

	pygame.display.flip()