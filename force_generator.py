from vector3 import Vector3
import math,pygame

class ParticleForceGenerator():
	def update_force(particle,dt =  None):
		raise NotImplementedError()

class ParticleForceRegistry():
	class ParticleForceRegistration():
		def __init__(self,particle,fg):
			self.particle = particle
			self.fg = fg

	def __init__(self):
		self.registry = []

	def add(self,particle,fg):
		self.registry.append(self.ParticleForceRegistration(particle,fg))

	def remove(self,particle,fg):
		self.registry = [i for i in self.registry
						  if i.particle != particle
						  and i.fg != fg]

	def clear(self):
		self.registry.clear()

	def update_forces(self):
		for i in self.registry:
			i.fg.update_force(i.particle)

class ParticleGravity(ParticleForceGenerator):
	def __init__(self,gravity):
		super().__init__()
		self.gravity = gravity

	def update_force(self,particle,dt = None):
		mass = particle.get_mass()
		if mass == "Infinte":
			pass
		else:
			self.gravity.scale_vector(mass)
			particle.apply_force(self.gravity)

class ParticleDrag(ParticleForceGenerator):
	def __init__(self,k1,k2):
		self.k1 = k1
		self.k2 = k2

	def update_force(self,particle,dt = None):
		force = particle.velocity.copy()
		drag_constant = force.get_magnitude()
		drag_constant = drag_constant * self.k1 + (drag_constant**2) * self.k2

		force.normalize()
		force.scale_vector(-drag_constant)
		particle.apply_force(force)

class ParticleSpring(ParticleForceGenerator):
	def __init__(self,other_particle,spring_constant,natural_length):
		self.other = other_particle.position.copy()
		self.spring_constant = spring_constant
		self.natural_length = natural_length

	def update_force(self,particle,dt = None):
		# f = -k(|d| - l)d^
		distance = particle.position.get_added_vector(self.other,-1)
		real_magnitude = distance.get_magnitude()
		magnitude = real_magnitude - self.natural_length
		force = distance.get_normalized()
		force.scale_vector(-self.spring_constant*magnitude)

		particle.apply_force(force)

class ParticleAnchoredSpring(ParticleForceGenerator):
	def __init__(self,anchor_point,spring_constant,natural_length):
		self.anchor_point = anchor_point
		self.spring_constant = spring_constant
		self.natural_length = natural_length

	def update_force(self,particle,dt = None):
		distance = particle.position.get_added_vector(self.anchor_point,-1)
		real_magnitude = distance.get_magnitude()
		magnitude = real_magnitude - self.natural_length
		force = distance.get_normalized()
		force.scale_vector(-self.spring_constant*magnitude)

		particle.apply_force(force)

class ParticleBungee(ParticleForceGenerator):
	def __init__(self,other_particle,spring_constant,natural_length):
		self.other = other_particle.position.copy()
		self.spring_constant = spring_constant
		self.natural_length = natural_length

	def update_force(self,particle,dt = None):
		distance = particle.position.get_added_vector(self.other,-1)
		real_magnitude = distance.get_magnitude()
		magnitude = real_magnitude - self.natural_length
		if magnitude < self.natural_length:
			force = distance.get_normalized()
			force.scale_vector(-self.spring_constant*magnitude)
		else:
			force = Vector3()

		particle.apply_force(force)

class ParticleBuoyancy(ParticleForceGenerator):
	def __init__(self,water_height,submersion_depth,object_volume,liquid_density = 1000):
		self.water_height = water_height
		self.submersion_depth = submersion_depth
		self.liquid_density = liquid_density
		self.object_volume = object_volume

	def update_force(self,particle,dt = None):
		y_particle = particle.position.y * 100
		force = Vector3()

		if (y_particle <= self.water_height - self.submersion_depth):
			pass

		elif (y_particle >= self.water_height + self.submersion_depth):
			force.y = self.object_volume * self.liquid_density

		else:
			d = (y_particle - self.water_height + self.submersion_depth) / (2*self.submersion_depth)
			force.y = d * self.object_volume * self.liquid_density

		force.scale_vector(-1)
		particle.apply_force(force)

class ParticleFakeSpring(ParticleForceGenerator):
	def __init__(self,anchor_point,spring_constant,damping):
		self.anchor_point = anchor_point
		self.spring_constant = spring_constant
		self.damping = damping

	def update_force(self,particle,dt = None):
		e = 2.71828

		# pi(pinitial) = particle_position - anchor position
		relative_pos = particle.position.get_added_vector(self.anchor_point,-1)
		# print(f"Pi: x: {relative_pos.x}, y: {relative_pos.y}")

		# gamma(γ) = 1/2* root(4k - d^2), k = spring_constant, d = damping
		if (4*self.spring_constant - self.damping**2) >= 0:
			gamma = 1/2 * math.sqrt(4*self.spring_constant - self.damping**2)
			# print(f"Gamma: {gamma}")
		else:
			return None

		# c = (d/2gamma * pi) + (1/gamma * particle_velocity)
		velocity = particle.velocity.copy()
		term_1 = relative_pos.get_scaled_vector(self.damping/(2*gamma))
		term_2 = velocity.get_scaled_vector(1/gamma)
		c = term_1.get_added_vector(term_2)
		# print(f"C: x:{c.x}, y:{c.y}")

		# pf(pfinal) = [pi cos(γ t) + c sin(γ t)]*e^((-d/2)*dt)
		term_1 = relative_pos.get_scaled_vector(math.cos(gamma*dt))
		term_2 = c.get_scaled_vector(math.sin(gamma*dt))
		term_3 = term_1.get_added_vector(term_2)
		final_pos = term_3.get_scaled_vector(e**((self.damping/2) * dt))
		# print(f"Pf: x: {final_pos.x}, y:{final_pos.y}")

		# acceleration = (pf - pi)/dt^2
		delta_d = final_pos.get_added_vector(relative_pos,-1)
		# print(f"Distance = {delta_d.get_magnitude()}")
		acceleration = delta_d.get_scaled_vector(1/(dt**2))
		# print(f"Acceleration: x: {acceleration.x}, y: {acceleration.y}")
		
		# print("------------------------------------------------")

		# force = ma
		mass = particle.get_mass()
		if mass:
			force = acceleration.get_scaled_vector(mass)
		else:
			force = Vector3()

		force.scale_vector(-1)
		# print(force.get_magnitude())
		particle.apply_force(force)