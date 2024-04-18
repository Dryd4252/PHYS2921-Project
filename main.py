from scipy import constants

class erbium_host_crystals():
	def __init__(
		self,
		name,
		reference,
		wavelength,
		optical_lifetime,
		branching_ratio,
		spontaneous_lifetime,
		oscilator_strength,
		dipole_moment,
		lifetime_limit,
		site_symmetry
	):
		self.name = name
		self.reference = reference
		self.wavelength = (wavelength * 1e-9) if wavelength is not None else None
		self.optical_lifetime = (optical_lifetime * 1e-3) if optical_lifetime is not None else None
		self.branching_ratio = branching_ratio
		self.spontaneous_lifetime = (spontaneous_lifetime * 1e-3) if optical_lifetime is not None else None
		self.oscilator_strength = oscilator_strength 
		self.dipole_moment = dipole_moment 
		self.lifetime_limit = lifetime_limit
		self.site_symmetry = site_symmetry

	def get_missing_values(self):
		missing_values = [attr for (attr, value) in self.__dict__.items() if value is None]


		if ("spontaneous_lifetime" in missing_values and 
			len(set(["optical_lifetime", "branching_ratio"]).intersection(missing_values)) == 0):
		
			self.solve_spontaneous_lifetime_2()
			missing_values.remove("spontaneous_lifetime")


		if ("dipole_moment" in missing_values and 
			len(set(["spontaneous_lifetime", "wavelength"]).intersection(missing_values)) == 0):
		
			self.solve_dipole_moment_2()
			missing_values.remove("dipole_moment")


		if ("optical_lifetime" in missing_values and 
			len(set(["branching_ratio", "spontaneous_lifetime"]).intersection(missing_values)) == 0):

			self.solve_optical_lifetime()
			missing_values.remove("optical_lifetime")


		if ("branching_ratio" in missing_values and 
			len(set(["optical_lifetime", "spontaneous_lifetime"]).intersection(missing_values)) == 0):
		
			self.solve_branching_ratio()
			missing_values.remove("branching_ratio")


		if ("oscilator_strength" in missing_values and 
			len(set(["dipole_moment", "wavelength"]).intersection(missing_values)) == 0):
		
			self.solve_oscilator_strength()
			missing_values.remove("oscilator_strength")


		if ("dipole_moment" in missing_values and 
			len(set(["oscilator_strength", "wavelength"]).intersection(missing_values)) == 0):
		
			self.solve_dipole_moment_1()
			missing_values.remove("dipole_moment")


		if ("spontaneous_lifetime" in missing_values and 
			len(set(["wavelength", "dipole_moment"]).intersection(missing_values)) == 0):

			self.solve_spontaneous_lifetime_1()
			missing_values.remove("spontaneous_lifetime")


		if ("lifetime_limit" in missing_values and 
			"optical_lifetime" not in missing_values):
		
			self.solve_lifetime_limit()
			missing_values.remove("lifetime_limit")


		print(f"Could not solve for: ", end = "")
		print(missing_values)


	def solve_spontaneous_lifetime_1(self):
		pass
		# T_spon = (3 * \epsilon_0 * \hbar * \lambda^3) / (8 * \pi^2 * n * \mu^2)
		# Don't know what to do with refractive index

		# numerator = 3 * constants.epsilon_0 * constants.hbar * (self.wavelength ** 3)
		# denominator = 8 * (constants.pi ** 2) * refractive_index * (self.dipole_moment ** 2)
		# self.spontaneous_lifetime = numerator / denominator

	def solve_dipole_moment_2(self):
		pass
		# \mu = sqrt( (3 * \epsilon_0 * \hbar * \lambda^3) / (8 * \pi^2 * n * T_spon) )
		# Don't know what to do with refractive index

		# numerator = 3 * constants.epsilon_0 * constants.hbar * (self.wavelength ** 3)
		# denominator = 8 * (constants.pi ** 2) * refractive_index * (self.dipole_moment ** 2)
		# self.dipole_moment = (numerator / denominator) ** 0.5

	def solve_optical_lifetime(self):
		# T_1 = Branching ratio * T_spon

		self.optical_lifetime = self.branching_ratio * self.spontaneous_lifetime	

	def solve_branching_ratio(self):
		# Branching ratio = T_1 / T_spon

		self.branching_ratio = self.optical_lifetime / self.spontaneous_lifetime

	def solve_spontaneous_lifetime_2(self):
		# T_spon = T_1  / Branching ratio

		self.spontaneous_lifetime = self.optical_lifetime / self.branching_ratio

	def solve_oscilator_strength(self):
		# f = (2 * \mu * m_e * \omega) / (\hbar * e^2)

		angular_frequency = 2 * constants.pi * constants.c / self.wavelength
		numerator = 2 * self.dipole_moment * constants.m_e * angular_frequency
		denominator = constants.hbar * (constants.e ** 2)

		self.oscilator_strength = numerator / denominator

	def solve_dipole_moment_1(self):
		# \mu = (\hbar * e^2 * f) / (2 * m_e * \omega)

		angular_frequency = 2 * constants.pi * constants.c / self.wavelength
		numerator = constants.hbar * (constants.e ** 2) * self.oscilator_strength
		denominator = 2 * constants.m_e * angular_frequency

		self.dipole_moment = numerator / denominator

	def solve_lifetime_limit(self):
		# \gamma_0 = 1 / (2\pi * T_1)

		self.lifetime_limit = 1 / (2 * constants.pi * self.optical_lifetime)

	def get_values(self):
		for (x,y) in self.__dict__.items():
			print(f"{x}: {y}")
			

def main():
	# (name, reference, wavelength(nm), optical_lifetime(ms), branching_ratio, spontaneous_lifetime(ms),
	#	oscilator_strength, dipole_moment(C/m), lifetime_limit(Hz), site_symmetry

	#Takes in usual values in the usual units. e.g. wavelength is usualy given in nm so expects nm

	#Fractional Uncertainty: 

	Y_2SiO_5 = erbium_host_crystals("Y_2SiO_5", "I made it up", 1536.47769, 11.4, 0.2, None, None, None, None, None)
	Y_2SiO_5.get_missing_values()
	Y_2SiO_5.get_values()

if __name__ == "__main__":
	main()