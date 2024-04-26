from scipy import constants

class erbium_host_crystals():
	def __init__(
		self,
		refractive_index: float,
		wavelength: float,
		optical_lifetime: float,
		branching_ratio: float,
		spontaneous_lifetime: float,
		dipole_moment: float,
		oscilator_strength: float,
		lifetime_limit: float,
	):
		self.refractive_index = refractive_index if refractive_index is not None else 2
		self.wavelength = (wavelength * 1e-9) if wavelength is not None else None
		self.optical_lifetime = (optical_lifetime * 1e-3) if optical_lifetime is not None else None
		self.branching_ratio = branching_ratio
		self.spontaneous_lifetime = (spontaneous_lifetime * 1e-3) if spontaneous_lifetime is not None else None
		self.dipole_moment = dipole_moment 
		self.oscilator_strength = oscilator_strength 
		self.lifetime_limit = lifetime_limit
		self.ignore_attributes = (
			"ignore_attributes", 
			"attribute_requiremnts"
		)
		self.attribute_requiremnts = {
		"spontaneous_lifetime": [
			(("optical_lifetime", "branching_ratio"), self.solve_spontaneous_lifetime_1),
			(("wavelength", "dipole_moment"), self.solve_spontaneous_lifetime_2)
			],
		"dipole_moment": [
			(("spontaneous_lifetime", "wavelength"), self.solve_dipole_moment_2),
			(("oscilator_strength", "wavelength"), self.solve_dipole_moment_1)
			],
		"optical_lifetime": (("branching_ratio", "spontaneous_lifetime"), self.solve_optical_lifetime),
		"branching_ratio": (("optical_lifetime", "spontaneous_lifetime"), self.solve_branching_ratio),
		"oscilator_strength": (("dipole_moment", "wavelength"), self.solve_oscilator_strength),
		"lifetime_limit": (("optical_lifetime"), self.solve_lifetime_limit)
		}

	def get_values(self):
		for (x,y) in self.__dict__.items():
			if x in self.ignore_attributes: continue
			print(f"{x}: {y}")

	def get_missing_values(self):
		missing_values = [attr for (attr, value) in self.__dict__.items() 
			if value is None and attr not in self.ignore_attributes]

		for (attr, value) in self.__dict__.items():
			if attr in self.ignore_attributes:
				continue
			if value is None:
				if type(self.attribute_requiremnts[attr]) is list:
					for requirments in self.attribute_requiremnts[attr]:
						required_attributes =  set(requirments[0])
						if len(required_attributes & set(missing_values)) == 0:
							requirments[1]()
							missing_values.remove(attr)
				else:
					requirments = self.attribute_requiremnts[attr]
					required_attributes =  set(requirments[0])
					if len(required_attributes & set(missing_values)) == 0:
						requirments[1]()
						missing_values.remove(attr)

	def solve_spontaneous_lifetime_1(self):
		# T_spon = T_1  / Branching ratio

		self.spontaneous_lifetime = self.optical_lifetime / self.branching_ratio

	def solve_dipole_moment_1(self):
		# \mu = (\hbar * e^2 * f) / (2 * m_e * \omega)

		angular_frequency = 2 * constants.pi * constants.c / self.wavelength
		numerator = constants.hbar * (constants.e ** 2) * self.oscilator_strength
		denominator = 2 * constants.m_e * angular_frequency

		self.dipole_moment = numerator / denominator

	def solve_spontaneous_lifetime_2(self):

		angular_frequency = 2 * constants.pi * constants.c / self.wavelength
		numerator = 3 * constants.epsilon_0 * constants.c * (self.wavelength ** 2) * constants.hbar
		denominator = 4 * constants.pi * self.refractive_index * (self.dipole_moment ** 2) * angular_frequency
		refractive_index_modifier = (2 * (self.refractive_index ** 2) + 1) / (3 * (self.refractive_index ** 2))
		self.spontaneous_lifetime = (numerator / denominator) * (refractive_index_modifier ** 2)

	def solve_dipole_moment_2(self):

		angular_frequency = 2 * constants.pi * constants.c / self.wavelength
		numerator = 3 * constants.epsilon_0 * constants.c * (self.wavelength ** 2) * constants.hbar
		denominator = 4 * constants.pi * self.refractive_index * self.spontaneous_lifetime * angular_frequency
		refractive_index_modifier = (2 * (self.refractive_index ** 2) + 1) / (3 * (self.refractive_index ** 2))
		self.dipole_moment = ((numerator / denominator) ** 0.5) * refractive_index_modifier

	def solve_optical_lifetime(self):
		# T_1 = Branching ratio * T_spon

		self.optical_lifetime = self.branching_ratio * self.spontaneous_lifetime	

	def solve_branching_ratio(self):
		# Branching ratio = T_1 / T_spon

		self.branching_ratio = self.optical_lifetime / self.spontaneous_lifetime

	def solve_oscilator_strength(self):
		# f = (2 * \mu * m_e * \omega) / (\hbar * e^2)

		angular_frequency = 2 * constants.pi * constants.c / self.wavelength
		numerator = 2 * self.dipole_moment * constants.m_e * angular_frequency
		denominator = constants.hbar * (constants.e ** 2)

		self.oscilator_strength = numerator / denominator

	def solve_lifetime_limit(self):
		# \gamma_0 = 1 / (2\pi * T_1)

		self.lifetime_limit = 1 / (2 * constants.pi * self.optical_lifetime)


def main():
	# (wavelength(nm), optical_lifetime(ms), branching_ratio, spontaneous_lifetime(ms),
	#	oscilator_strength, dipole_moment(C/m), lifetime_limit(Hz), site_symmetry

	#Takes in usual values in the usual units. e.g. wavelength is usualy given in nm so expects nm

	#Outputs values in SI units

	#Fractional Uncertainty: 

	Y_2SiO_5 = erbium_host_crystals(None, 1536.47769, 11.4, 0.2, None, None, None, None)
	Y_2SiO_5.get_missing_values()
	Y_2SiO_5.get_values()

if __name__ == "__main__":
	main()