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
position = screen_to_world((400,10))
p_1.position = Vector3(*position,0)
p_1.acceleration = Vector3(0,10,0)
# p_1.inverse_mass = 1/100000000000000000
p_1.velocity = Vector3(0,0,0)

p_2 = SphereParticle(20)
position = screen_to_world((400,130))
p_2.position = Vector3(*position,0)
p_2.acceleration = Vector3(0,0,0)
p_2.inverse_mass = 1/1000000000000000
p_2.velocity = Vector3(0,0,0)

contact = ParticleContact(p_1,p_2,0.5)

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

	# This took 2 DAYS!!!!!!!!!!! (somehow)

	# The update should be called before the contact resolve function (necessary)
	p_1.update(dt)
	p_2.update(dt)

	# Drawing the particles
	position = world_to_screen((p_1.position.x,p_1.position.y))
	pygame.draw.circle(screen,"white",position,p_1.radius)
	position = world_to_screen((p_2.position.x,p_2.position.y))
	pygame.draw.circle(screen,"red",position,p_2.radius)

	# Finding the penetration between the particles
	dist = math.sqrt((p_1.position.x - p_2.position.x)**2 + (p_1.position.y - p_2.position.y)**2)
	penetration = (p_1.radius/PIXELS_PER_METER + p_2.radius/PIXELS_PER_METER) - dist
	
	# Finding the distance by which particles will get closer in next frame
	acc_1 = p_1.acceleration.get_added_vector(p_1.force_accum,p_1.inverse_mass)
	acc_2 = p_2.acceleration.get_added_vector(p_2.force_accum,p_2.inverse_mass)
	rel_vel = acc_1.get_added_vector(acc_2,-1).get_scaled_vector(dt)
	distance = rel_vel.get_scaled_vector(dt).get_magnitude()

	# If this is true then it means that  the particle will collide after one frame
	# This is necessary to detect collision one frame earlier
	if penetration + distance >= 0:
		contact = ParticleContact(p_1,p_2,0.5)
		contact.resolve(penetration,dt)

	pygame.display.flip()