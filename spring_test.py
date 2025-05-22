import pygame,sys,time
from vector3 import Vector3
from particle import Particle
from force_generator import ParticleFakeSpring

pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 800, 600
PIXELS_PER_METER = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Window")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Ubuntu",20)

def world_to_screen(pos):
    return (pos[0] * PIXELS_PER_METER, pos[1] * PIXELS_PER_METER)

def screen_to_world(pos):
    return (pos[0] / PIXELS_PER_METER, pos[1] / PIXELS_PER_METER)

pos = screen_to_world((400,400))
anchor = Vector3(*pos,0)
fake_spring_1 = ParticleFakeSpring(anchor,500000,100)
# fake_spring_2 = ParticleFakeSpring(anchor,200,5)
pos = screen_to_world((400,100))
particle = Particle(position = Vector3(*pos,0),gravity = Vector3(0,0,0))
# p = Particle(position = Vector3(*pos,0),gravity = Vector3(0,0,0))

previous_time = time.time()
while True:
	dt = time.time() - previous_time
	previous_time = time.time()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill((100,100,100))
	text = font.render(f"{(1/dt):.2f}","black",False)
	screen.blit(text,(0,0))

	fake_spring_1.update_force(particle,dt)
	# fake_spring_2.update_force(p,dt)
	particle.update(dt)
	# p.update(dt)

	position = screen_to_world(pygame.mouse.get_pos())
	anchor = Vector3(*position,0)
	fake_spring_1 = ParticleFakeSpring(anchor,500000,100)
	# fake_spring_2 = ParticleFakeSpring(anchor,200,5)

	position = world_to_screen((anchor.x,anchor.y))
	pygame.draw.circle(screen,"white",position,10)
	position = world_to_screen((particle.position.x,particle.position.y))
	pygame.draw.circle(screen,"red",position,10)
	# position = world_to_screen((p.position.x,p.position.y))
	# pygame.draw.circle(screen,"green",position,10)
	
	pygame.display.flip()
	# clock.tick(1)