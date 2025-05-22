from random import uniform
from particle import Particle
from vector3 import Vector3

class Firework(Particle):
	def __init__(self,type,age,damping,mass,gravity,radius):
		super().__init__(damping = damping,mass = mass,gravity = gravity)
		self.type = type
		self.age = age
		self.radius = radius

class Payload():
	def __init__(self,firework_type,count):
		self.type = firework_type
		self.count = count

class FireworkRule():
	def __init__(self,type,min_age,max_age,min_velocity,max_velocity,damping,gravity,radius):
		self.type = type
		self.min_age = min_age
		self.max_age = max_age
		self.min_velocity = min_velocity
		self.max_velocity = max_velocity
		self.damping = damping
		self.gravity = gravity
		self.radius = radius
		self.payloads = []

	def create_firework(self,parent_position):
		age = uniform(self.min_age,self.max_age)
		velocity = Vector3(
							uniform(self.min_velocity.x,self.max_velocity.x),
							uniform(self.max_velocity.y,self.min_velocity.y),
							uniform(self.min_velocity.z,self.max_velocity.z)
			)
		firework = Firework(
							type = self.type,
							age = age,
							damping = self.damping,
							mass = 1,
							gravity = self.gravity,
							radius = self.radius
							)
		firework.velocity = velocity
		firework.position = Vector3(parent_position.x,parent_position.y,parent_position.z)

		return firework

def explode_firework(firework, rules):
	if firework.type < len(rules):
		rule = rules.get(firework.type)
		if rule:
			new_fireworks = []
			for payload in rule.payloads:
				for _ in range(payload.count):
					if payload.type < len(rules):
						pos = (firework.position.x,firework.position.y)
						# print(pos)
						new_fw = rules[payload.type].create_firework(Vector3(*pos,0))
						new_fireworks.append(new_fw)

			# print()
			return new_fireworks
	# print()
	return []

rules = {}
rocket_rule = FireworkRule(
				type = 0,
				min_age = 7,
				max_age = 8,
				min_velocity = Vector3(0,-5,0),
				max_velocity = Vector3(0,-10,0),
				damping = 0.6,
				gravity = Vector3(0,5,0),
				radius = 10
	)
rocket_rule.payloads.append(Payload(firework_type = 1,count=20))
rules[0] = rocket_rule

burst_rule = FireworkRule(
				type = 1,
				min_age = 5,
				max_age = 7,
				min_velocity = Vector3(-5,-5,0),
				max_velocity = Vector3(5,5,0),
				damping = 0.1,
				gravity = Vector3(0,5,0),
				radius = 5
	)
burst_rule.payloads.append(Payload(firework_type = 2,count = 30))
rules[1] = burst_rule