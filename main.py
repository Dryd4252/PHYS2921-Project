from scipy import constants
from uncertainties import ufloat

class erbium_host_crystals():
	def __init__(
		self,
		wavelength: float,
		wavelength_unc: float,
		optical_lifetime: float,
		optical_lifetime_unc: float,
		branching_ratio: float,
		branching_ratio_unc: float,
		dipole_moment: float,
		dipole_moment_unc: float,
		spontaneous_lifetime: float,
		spontaneous_lifetime_unc: float,
		lifetime_limit: float,
		lifetime_limit_unc: float,
		oscilator_strength: float,
		oscilator_strength_unc: float,
		refractive_index: float,
		refractive_index_unc: float
	):	
		refractive_index = 2 if refractive_index is None else refractive_index
		self.refractive_index =  self.set_value(refractive_index, refractive_index_unc)

		wavelength = (wavelength * 1e-9) if wavelength is not None else None
		self.wavelength =  self.set_value(wavelength, wavelength_unc)

		optical_lifetime = (optical_lifetime * 1e-3) if optical_lifetime is not None else None
		self.optical_lifetime = self.set_value(optical_lifetime, optical_lifetime_unc)

		self.branching_ratio = self.set_value(branching_ratio, branching_ratio_unc)

		spontaneous_lifetime = (spontaneous_lifetime * 1e-3) if spontaneous_lifetime is not None else None
		self.spontaneous_lifetime = self.set_value(spontaneous_lifetime, spontaneous_lifetime_unc)

		self.dipole_moment = self.set_value(dipole_moment, dipole_moment_unc)

		self.oscilator_strength = self.set_value(oscilator_strength, oscilator_strength_unc)

		self.lifetime_limit = self.set_value(lifetime_limit, lifetime_limit_unc)

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

		self.get_missing_values()

	@staticmethod
	def set_value(value, unc):
		if value is None:
			return None
		if unc is None:
			s = str(float(value))
			if 'e' in s:
				parts = s.split("e")
				significance = int(parts[1])
				unc = 10 ** significance
			else:
				parts = s.split(".")
				significance = -1 * len(parts[1]) if len(parts) == 2 else 0
				unc = 10 ** significance
		return ufloat(value, unc)

	def get_values(self):
		ordered_attributes = []
		ordered_attributes.append(self.wavelength.n if self.wavelength is not None else None)
		ordered_attributes.append(self.wavelength.s if self.wavelength is not None else None)
		ordered_attributes.append(self.optical_lifetime.n if self.optical_lifetime is not None else None)
		ordered_attributes.append(self.optical_lifetime.s if self.optical_lifetime is not None else None)
		ordered_attributes.append(self.branching_ratio.n if self.branching_ratio is not None else None)
		ordered_attributes.append(self.branching_ratio.s if self.branching_ratio is not None else None)
		ordered_attributes.append(self.dipole_moment.n if self.dipole_moment is not None else None)
		ordered_attributes.append(self.dipole_moment.s if self.dipole_moment is not None else None)
		ordered_attributes.append(self.spontaneous_lifetime.n if self.spontaneous_lifetime is not None else None)
		ordered_attributes.append(self.spontaneous_lifetime.s if self.spontaneous_lifetime is not None else None)
		ordered_attributes.append(self.lifetime_limit.n if self.lifetime_limit is not None else None)
		ordered_attributes.append(self.lifetime_limit.s if self.lifetime_limit is not None else None)
		ordered_attributes.append(self.oscilator_strength.n if self.oscilator_strength is not None else None)
		ordered_attributes.append(self.oscilator_strength.s if self.oscilator_strength is not None else None)
		ordered_attributes.append(self.refractive_index.n if self.refractive_index is not None else None)
		ordered_attributes.append(self.refractive_index.s if self.refractive_index is not None else None)
		return ordered_attributes

	def print_values(self):
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
							break
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
		numerator = 2 * (self.dipole_moment ** 2) * constants.m_e * angular_frequency
		denominator = constants.hbar * (constants.e ** 2)

		self.oscilator_strength = numerator / denominator

	def solve_lifetime_limit(self):
		# \gamma_0 = 1 / (2\pi * T_1)

		self.lifetime_limit = 1 / (2 * constants.pi * self.optical_lifetime)


def main():
	#Takes in usual values in the usual units. e.g. wavelength is usualy given in nm so expects nm

	#Outputs values in SI units

	#erbium_host_crystal.get_values() returns an array in order of all the attibutes.

	#Fractional Uncertainty: 

	# Values required
	# 	wavelength: float,
	# 	wavelength_unc: float,
	# 	optical_lifetime: float,
	# 	optical_lifetime_unc: float,
	# 	branching_ratio: float,
	# 	branching_ratio_unc: float,
	# 	dipole_moment: float,
	# 	dipole_moment_unc: float,
	# 	spontaneous_lifetime: float,
	# 	spontaneous_lifetime_unc: float,
	# 	lifetime_limit: float,
	# 	lifetime_limit_unc: float,
	# 	oscilator_strength: float,
	# 	oscilator_strength_unc: float,
	# 	refractive_index: float,
	# 	refractive_index_unc: float

	# Y_2SiO_5 = erbium_host_crystals(1536.4776, None, 11.4, None, 0.2, None, None, None, None, None, None, None, None, None, None, None)
	# Y_2SiO_5.print_values()
	# print(Y_2SiO_5.get_values())

	YVO_4 = erbium_host_crystals(1529.21, None, 3.34, None, 0.415, None, 1.00E-32, None, None, None, None, None, None, None, None, None)
	# YVO_4.print_values()
	print(YVO_4.get_values())


if __name__ == "__main__":
	main()