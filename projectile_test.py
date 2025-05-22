import pygame, sys, time
from random import choice
from vector3 import Vector3
from particle import Particle

pygame.init()
pygame.font.init()

WIDTH,HEIGHT = 800, 400
PIXELS_PER_METER = 100
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Engine")
font = pygame.font.SysFont("notosansoriya",20)

test_vector = Vector3()
mass,gravity = 10, 10
test_particle = Particle(mass = mass, gravity = gravity)
apply_force = False
shots = []
shot_types = ["Pistol","Artillery","Fireball","Laser"]

projectiles = {
	"Pistol":{
			"mass":2,
			"velocity":(35,0,0),
			"acceleration":(0,1,0),
			"damping":0.995
	},
	"Artillery":{
			"mass":200,
			"velocity":(40,-30,0),
			"acceleration":(0,20,0),
			"damping":0.995
	},
	"Fireball":{
			"mass":1,
			"velocity":(10,0,0),
			"acceleration":(0,6,0),
			"damping":0.9
	},
	"Laser":{
			"mass":0.1,
			"velocity":(100,0,0),
			"acceleration":(0,0,0),
			"damping":0.99
	}
}

# Functions 
def render_frames(dt):
	text = font.render(f"{(1/dt):.2f}","black",False)
	screen.blit(text,(0,0))

def get_scaled_vector(vector,k):
	return (vector.x * k, vector.y * k, vector.z * k)

def get_component_product(vector1,vector2):
	return (vector1.x * vector2.x, vector1.y * vector2.y, vector1.z * vector2.z)

def get_scalar_product(vector1,vector2):
	return (vector1.x * vector2.x + vector1.y * vector2.y + vector1.z * vector2.z)

def get_vector_product(vector1,vector2):
	x = vector1.y*vector2.z - vector1.z*vector2.y
	y = vector1.z*vector2.x - vector1.x*vector2.z
	z = vector1.x*vector2.y - vector1.y*vector2.x

	return (x,y,z)

def screen_to_world(x,y):
	return (x/PIXELS_PER_METER,y/PIXELS_PER_METER)

def world_to_screen(x,y):
	return (x*PIXELS_PER_METER,y*PIXELS_PER_METER)

def create_shot(shot_type,pos):
	particle = Particle()
	projectile = projectiles[shot_type]
	particle.inverse_mass = 1/projectile["mass"]
	particle.velocity = Vector3(*projectile["velocity"])
	particle.acceleration = Vector3(*projectile["acceleration"])
	particle.damping = projectile["damping"]
	particle.position = Vector3(*screen_to_world(*pos),0)

	return particle

previous_time = time.time()
while True:
	dt = time.time() - previous_time
	previous_time = time.time()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 3:
				apply_force = not apply_force
			elif event.button == 1:
				# shot_type = choice(shot_types)
				shot_type = shot_types[2]
				pos = pygame.mouse.get_pos()
				shots.append((create_shot(shot_type,pos),time.time()))

	print(len(shots))
	screen.fill((100,100,100))
	render_frames(dt)

	for projectile in shots[:]:
		shot = projectile[0]
		shot.update(dt)
		x = (shot.position.x)
		y = (shot.position.y)
		x_w, y_w = world_to_screen(x,y)
		pygame.draw.circle(screen,"white",(x_w,y_w),20)

		if y_w < 0 or x_w > WIDTH or time.time() - projectile[1] > 5000:
			shots.remove(projectile)
		
	# test_particle.update(dt)
	# if apply_force:
	# 	test_particle.apply_force(Vector3(y=-mass*gravity))

	# test_particle.update(dt)
	# pygame.draw.circle(screen,"white",(test_particle.position.x,test_particle.position.y),20)

	pygame.display.update()