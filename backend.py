from enum import auto, Enum
from typing import Tuple, Optional
from numpy import linalg as ila
from colorist import ColorHex
from colorama import Fore
import numpy as np
import copy


CLEAR = Fore.RESET

class Colour(Enum):
	GREY = ColorHex("#777").generate_ansi_code()
	BLUE = ColorHex("#8ca7ff").generate_ansi_code()
	RED = ColorHex("#ff8c98").generate_ansi_code()
	GREEN = ColorHex("#60a86c").generate_ansi_code()

class HealthStatus(Enum):
	SUSCEPTIBLE = Colour.GREEN.value
	INFECTED = Colour.RED.value
	RECOVERED = Colour.BLUE.value # new normal isn't quite green
	DECEASED =  Colour.GREY.value

	def __str__(self):
		return self.value + self.name + CLEAR

class Blob:
	_position:np.ndarray
	_velocity:np.ndarray
	_acceleration:np.ndarray

	def __init__(self, initial_position:Tuple[float,float], ID:int, health_status:Optional[HealthStatus]=None) -> None:
		if health_status is None:
			health_status = HealthStatus.SUSCEPTIBLE

		self.id = ID
		self._position = np.array(initial_position)
		self.health_status = health_status

	def update_position(self, delta_t:float):
		''' use a linear approximation or n_degree derivative to predict motion after some unit time. 
		A value of `delta_t=1` refers to moving 1 frame forward.
		'''
		self._position += self._velocity * delta_t
	
	def update_velocity(self, delta_t:float):
		self._acceleration += self._acceleration * delta_t
	
	def update_acceleration(self, ticks):
		# take things like collisions, friction, etc, to decide whether the acceleration should change, and by how much
		# might also change the acceleration randomly every few ticks to make them walk around randomly 
		# could also model this on desmos

		new_acceleration = copy.deepcopy(self._acceleration)
		...
		self._acceleration = new_acceleration
	
	def get_position(self): return self._position
	def get_velocity(self): return self._velocity
	def get_acceleration(self): return self._acceleration
	def set_position(self, position:Tuple[float,float]): self._position = np.array(position)
	def set_velocity(self, velocity:Tuple[float,float]): self._velocity = np.array(velocity)
	def set_acceleration(self, acceleration:Tuple[float,float]): self._acceleration = np.array(acceleration)