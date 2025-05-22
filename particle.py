from vector3 import Vector3

class Particle():
	def __init__(self,
				mass=10,
				damping=0.885,
				gravity = Vector3(0,70,0),
				position=Vector3(100,0,0)):

		self.position = position
		self.velocity = Vector3()
		self.acceleration = gravity
		self.force_accum = Vector3()
		self.damping = damping
		if mass > 0:
			self.inverse_mass = 1/mass
		else:
			self.inverse_mass = 1

	def update(self,dt):
		# Update linear position
		self.position.add_vector(self.velocity,dt)

		# Update acceleration
		acceleration = self.acceleration.copy()
		# acceleration = Vector3()
		acceleration.add_vector(self.force_accum,self.inverse_mass)

		# Add damping and updating velocity
		self.velocity.add_vector(acceleration,dt)
		self.velocity.scale_vector(self.damping**dt)

		self.force_accum.zero()

	def apply_force(self,force):
		self.force_accum.add_vector(force)

	def get_mass(self):
		if self.inverse_mass == 0:
			return None
		else:
			return 1/self.inverse_mass