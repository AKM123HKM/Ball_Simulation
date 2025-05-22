import pygame,sys,time
from vector3 import Vector3
from particle import SphereParticle
from contacts import ParticleContact
import math

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
PIXELS_PER_METER = 100

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Collision Test")
font = pygame.font.SysFont("Ubuntu",20)

def world_to_screen(pos):
    return (pos[0] * PIXELS_PER_METER, pos[1] * PIXELS_PER_METER)

def screen_to_world(pos):
    return (pos[0] / PIXELS_PER_METER, pos[1] / PIXELS_PER_METER)

p_1 = SphereParticle(10)
position = screen_to_world((400,100))
p_1.position = Vector3(*position,0)
p_1.acceleration = Vector3(0,0,0)
# p_1.inverse_mass = 1/100000000000000000
p_1.velocity = Vector3(0,10,0)

p_2 = SphereParticle(20)
position = screen_to_world((400,300))
p_2.position = Vector3(*position,0)
p_2.acceleration = Vector3(0,0,0)
p_2.velocity = Vector3(0,-10,0)

contact = ParticleContact(p_1,p_2,0.8)

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

	dist = math.sqrt((p_1.position.x - p_2.position.x)**2 + (p_1.position.y - p_2.position.y)**2)
	penetration = (p_1.radius/PIXELS_PER_METER + p_2.radius/PIXELS_PER_METER) - dist
	if penetration >= 0:
		# print(p_1.velocity.y,p_2.velocity.y)
		contact = ParticleContact(p_1,p_2,0.8)
		contact.resolve(penetration)
		# print(p_1.velocity.y,p_2.velocity.y)

	p_1.update(dt)
	p_2.update(dt)

	position = world_to_screen((p_1.position.x,p_1.position.y))
	pygame.draw.circle(screen,"white",position,p_1.radius)
	position = world_to_screen((p_2.position.x,p_2.position.y))
	pygame.draw.circle(screen,"red",position,p_2.radius)

	pygame.display.flip()