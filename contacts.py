from vector3 import Vector3

class ParticleContact():
	def __init__(self,particle_1,particle_2,restitution):
		self.particle_1 = particle_1
		self.particle_2 = particle_2
		self.restitution = restitution
		self.contact_normal = Vector3()

	def calculate_seperating_velocity(self):
		delta_v = self.particle_1.velocity.get_added_vector(self.particle_2.velocity,-1)
		self.contact_normal = self.particle_1.position.get_added_vector(self.particle_2.position,-1).get_normalized()
		seperating_velocity = delta_v.get_dot_product(self.contact_normal)
		return seperating_velocity

	def resolve(self,penetration):
		seperating_velocity = self.calculate_seperating_velocity()
		self.resolve_penetration(penetration)

		if seperating_velocity > 0:
			return None

		new_seperating_velocity = self.restitution*seperating_velocity*-1

		delta_vel = new_seperating_velocity - seperating_velocity

		total_inverse_mass = self.particle_1.inverse_mass + self.particle_2.inverse_mass

		if total_inverse_mass <= 0:
			return None

		total_impulse = delta_vel / total_inverse_mass

		impulse_per_I_mass = self.contact_normal.get_scaled_vector(total_impulse)

		self.particle_1.velocity.add_vector(impulse_per_I_mass.get_scaled_vector(self.particle_1.inverse_mass))
		self.particle_2.velocity.add_vector(impulse_per_I_mass.get_scaled_vector(-self.particle_2.inverse_mass))

	def resolve_penetration(self,penetration):
		total_inverse_mass = self.particle_1.inverse_mass + self.particle_2.inverse_mass
		delta_1 = self.contact_normal.get_scaled_vector((self.particle_1.inverse_mass/total_inverse_mass)*penetration)
		delta_2 = self.contact_normal.get_scaled_vector((self.particle_2.inverse_mass/total_inverse_mass)*penetration)

		self.particle_1.position.add_vector(delta_1)
		self.particle_2.position.add_vector(delta_2,-1)