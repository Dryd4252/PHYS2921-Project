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
		refractive_index_unc: float,
		site_symetry: str,
		site_symetry_order: int,
		normalised_lifetime: float,
		normalised_lifetime_unc: float,
	):	
		refractive_index = 2 if refractive_index is None else refractive_index
		self.refractive_index =  self.set_value(refractive_index, refractive_index_unc)

		self.wavelength =  self.set_value(wavelength, wavelength_unc)
		self.wavelength = self.wavelength * 1e-9 if self.wavelength is not None else None

		self.optical_lifetime = self.set_value(optical_lifetime, optical_lifetime_unc)
		self.optical_lifetime = (self.optical_lifetime * 1e-3 
							if self.optical_lifetime is not None else None)

		self.branching_ratio = self.set_value(branching_ratio, branching_ratio_unc)

		self.spontaneous_lifetime = self.set_value(spontaneous_lifetime, spontaneous_lifetime_unc)
		self.spontaneous_lifetime = (self.spontaneous_lifetime * 1e-3 
							if self.spontaneous_lifetime is not None else None)

		self.dipole_moment = self.set_value(dipole_moment, dipole_moment_unc)

		self.oscilator_strength = self.set_value(oscilator_strength, oscilator_strength_unc)

		self.lifetime_limit = self.set_value(lifetime_limit, lifetime_limit_unc)


		self.ignore_attributes = (
			"ignore_attributes", 
			"attribute_requiremnts",
			"site_symetry_dict",
			"calculated_attributes",
		)

		self.calculated_attributes = set()

		self.site_symetry_dict = {
			"O_h": -6,
			"D_4h": -5,
			"T_h": -5,
			"O": -5,
			"T_d": -5,
			"D_6h": -5,
			"C_4h": -4,
			"D_4": -4,
			"D_2d": -4,
			"C_4v": -4,
			"D_2h": -4,
			"T": -4,
			"D_6": -4,
			"C_6h": -4,
			"C_6v": -4,
			"D_3d": -4,
			"D_3h": -4,
			"S_4": -3,
			"C_4": -3,
			"D_2": -3,
			"C_2h": -3,
			"C_2v": -3,
			"C_6": -3,
			"C_3i": -3,
			"D_3": -3,
			"C_3v": -3,
			"C_3h": -3,
			"C_i": -2,
			"C_2": -2,
			"C_s": -2,
			"C_1h": -2,
			"C_3": -2,
			"C_1": -1,

		}

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
		"lifetime_limit": (("optical_lifetime",), self.solve_lifetime_limit)
		}

		self.get_missing_values()

		for x in self.calculated_attributes:
			if x == "refractive_index":
				self.refractive_index *= -1
			elif x == "wavelength":
				self.wavelength *= -1
			elif x == "optical_lifetime":
				self.optical_lifetime *= -1
			elif x == "branching_ratio":
				self.branching_ratio *= -1
			elif x == "spontaneous_lifetime":
				self.spontaneous_lifetime *= -1
			elif x == "dipole_moment":
				self.dipole_moment *= -1
			elif x == "oscilator_strength":
				self.oscilator_strength *= -1
			elif x == "lifetime_limit":
				self.lifetime_limit *= -1							

		self.site_symetry = site_symetry		

		if self.site_symetry not in self.site_symetry_dict:
			print(f"site_symetry [{self.site_symetry}] not found")
			self.site_symetry = None
		else :
			self.site_symetry_order = self.site_symetry_dict[self.site_symetry]

		self.normalised_lifetime = -1 * self.optical_lifetime * self.refractive_index if self.optical_lifetime != None else None

		
		self.wavelength = self.wavelength * 1e9 if self.wavelength != None else None
		self.optical_lifetime = self.optical_lifetime * 1e3 if self.optical_lifetime != None else None
		self.spontaneous_lifetime = self.spontaneous_lifetime * 1e3 if self.spontaneous_lifetime != None else None

	@staticmethod
	def set_value(value, unc):
		if value is None:
			return None
		if unc is None:
			s = str(float(value))
			if 'e' in s:
				parts = s.split("e")
				significance = int(parts[1])
				unc = (10 ** significance)/2
			else:
				parts = s.split(".")
				significance = -1 * len(parts[1]) if len(parts) == 2 else 0
				unc = (10 ** significance)/2
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
		ordered_attributes.append(self.site_symetry if self.refractive_index is not None else None)
		ordered_attributes.append(self.site_symetry_order if self.refractive_index is not None else None)
		ordered_attributes.append(self.normalised_lifetime.n if self.normalised_lifetime.n is not None else None)
		ordered_attributes.append(self.normalised_lifetime.s if self.normalised_lifetime.s is not None else None)
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
			if value is None and attr in list(self.attribute_requiremnts):
				if type(self.attribute_requiremnts[attr]) is list:
					for requirments in self.attribute_requiremnts[attr]:
						required_attributes =  set(requirments[0])
						if len(required_attributes & set(missing_values)) == 0:
							requirments[1]()
							missing_values.remove(attr)
							self.calculated_attributes.add(attr)
							break
				else:
					requirments = self.attribute_requiremnts[attr]
					required_attributes =  set(requirments[0])
					if len(required_attributes & set(missing_values)) == 0:
						requirments[1]()
						missing_values.remove(attr)
						self.calculated_attributes.add(attr)


	def solve_spontaneous_lifetime_1(self):
		# T_spon = T_1  / Branching ratio

		self.spontaneous_lifetime = (self.optical_lifetime / self.branching_ratio)

	def solve_dipole_moment_1(self):
		# \mu = (\hbar * e^2 * f) / (2 * m_e * \omega)

		angular_frequency = 2 * constants.pi * constants.c / self.wavelength
		numerator = constants.hbar * (constants.e ** 2) * self.oscilator_strength
		denominator = 2 * constants.m_e * angular_frequency

		self.dipole_moment = (numerator / denominator)

	def solve_spontaneous_lifetime_2(self):

		angular_frequency = 2 * constants.pi * constants.c / self.wavelength
		numerator = 3 * constants.epsilon_0 * constants.c * (self.wavelength ** 2) * constants.hbar
		denominator = 4 * constants.pi * self.refractive_index * (self.dipole_moment ** 2) * angular_frequency
		refractive_index_modifier = (2 * (self.refractive_index ** 2) + 1) / (3 * (self.refractive_index ** 2))
		self.spontaneous_lifetime = ((numerator / denominator) * (refractive_index_modifier ** 2))

	def solve_dipole_moment_2(self):
		angular_frequency = 2 * constants.pi * constants.c / self.wavelength
		numerator = 3 * constants.epsilon_0 * constants.c * (self.wavelength ** 2) * constants.hbar
		denominator = 4 * constants.pi * self.refractive_index * self.spontaneous_lifetime * angular_frequency
		refractive_index_modifier = (2 * (self.refractive_index ** 2) + 1) / (3 * (self.refractive_index ** 2))
		self.dipole_moment = ((numerator / denominator) ** 0.5) * refractive_index_modifier

	def solve_optical_lifetime(self):
		# T_1 = Branching ratio * T_spon

		self.optical_lifetime = (self.branching_ratio * self.spontaneous_lifetime)	

	def solve_branching_ratio(self):
		# Branching ratio = T_1 / T_spon

		self.branching_ratio = (self.optical_lifetime / self.spontaneous_lifetime)

	def solve_oscilator_strength(self):
		# f = (2 * \mu * m_e * \omega) / (\hbar * e^2)

		angular_frequency = 2 * constants.pi * constants.c / self.wavelength
		numerator = 2 * (self.dipole_moment ** 2) * constants.m_e * angular_frequency
		denominator = constants.hbar * (constants.e ** 2)

		self.oscilator_strength = (numerator / denominator)

	def solve_lifetime_limit(self):
		# \gamma_0 = 1 / (2\pi * T_1)

		self.lifetime_limit = (1 / (2 * constants.pi * self.optical_lifetime))


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

	#Calculated values will be returned with a negative sign.

								#wavelength   #lifetime   #branching ratio  #dipole moment
	YVO_4 = erbium_host_crystals(1533.90, None, None, None  , None, None     , None, None
								#spont_lifetime  #limit_lifetime  #oscilator_strength  refractive_index
								, None, None     , None, None     , None, None         , 1.88, None 
								#site symetry #site_symmetry_order  #normalised_lifetime
								, "S_4" 			, None 			, None , None)
	YVO_4.print_values()
	# print(YVO_4.get_values())


	#add normalised T_1 value with refractivce index, (n * T_1)
	


if __name__ == "__main__":
	main()