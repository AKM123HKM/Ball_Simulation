from math import sqrt

class Vector3():
	def __init__(self,x=0,y=0,z=0):
		self.x = x
		self.y = y
		self.z = z  
		self.coords = (self.x,self.y,self.z)

	def print_vector(self,x,y,font,screen):
		text = font.render(f"x:{self.x}, y:{self.y}, z:{self.z}","red",False)
		screen.blit(text,(x,y))

	def get_magnitude(self,squared = False):
		if squared:
			return (self.x**2 + self.y**2 + self.z**2)
		else:
			# print(self.x,self.y,self.z)
			return sqrt(self.x**2 + self.y**2 + self.z**2)

	def normalize(self):
		magnitude = self.get_magnitude()
		if not magnitude == 0:
			self.x /= magnitude
			self.y /= magnitude
			self.z /= magnitude

	def get_normalized(self):
		magnitude = self.get_magnitude()
		if not magnitude == 0:
			return Vector3(self.x / magnitude,
					self.y / magnitude,
					self.z / magnitude
					)
		return Vector3()

	def scale_vector(self,k):
		self.x *= k
		self.y *= k
		self.z *= k
		
	def get_scaled_vector(self,k):
		return Vector3(
			self.x * k,
			self.y * k,
			self.z * k
			)

	def add_vector(self,vector,scalar = 1):
		self.x += vector.x * scalar
		self.y += vector.y * scalar
		self.z += vector.z * scalar

	def get_added_vector(self,vector,scalar = 1):
		return Vector3(
			self.x + (vector.x * scalar),
			self.y + (vector.y * scalar),
			self.z + (vector.z * scalar)
			)

	def component_product(self,vector):
		self.x *= vector.x
		self.y *= vector.y
		self.z *= vector.z
	
	def get_component_product(self,vector):
		return Vector3(
			self.x * vector.x,
			self.y * vector.y,
			self.z * vector.z
			)

	def vector_prodcut(self,vector):
		self.x = self.y*vector.z - self.z*vector.y
		self.y = self.z*vector.x - self.x*vector.z
		self.z = self.x*vector.y - self.y*vector.x

	def get_vector_product(self,vector):
		return Vector3(
			self.y*vector.z - self.z*vector.y,
			self.z*vector.x - self.x*vector.z,
			self.x*vector.y - self.y*vector.x
			)

	def zero(self):
		self.x, self.y, self.z = 0, 0, 0

	def copy(self):
		return Vector3(self.x,self.y,self.z)