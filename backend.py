from enum import auto, Enum
from typing import Tuple, Optional
from numpy import linalg as ila
from colorist import ColorHex
from colorama import Fore
import numpy as np
import copy


CLEAR = Fore.RESET

class Colour(Enum):
	GREY = ColorHex("#777")
	BLUE = ColorHex("#8ca7ff")
	RED = ColorHex("#ff8c98")
	GREEN = ColorHex("#60a86c")

class HealthStatus(Enum):
	SUSCEPTIBLE = Colour.GREEN.value
	INFECTED = Colour.RED.value
	RECOVERED = Colour.BLUE.value
	DECEASED =  Colour.GREY.value

	
	def __str__(self):
		return self.value.generate_ansi_code() + self.name + CLEAR

class Blob:
	_position:np.ndarray
	_velocity:np.ndarray
	_acceleration:np.ndarray

	def __init__(self, initial_position:Tuple[float,float], ID:int, health_status:Optional[HealthStatus]=None,time_sick:Optional[int]=None) -> None:
		if health_status is None:
			health_status = HealthStatus.SUSCEPTIBLE

		self.id = ID
		self._position = np.array(initial_position)
		self._velocity = np.zeros_like(self._position)
		self._acceleration = np.zeros_like(self._position)
		self.health_status = health_status
		self.time_sick = 0 if time_sick is None else time_sick

	def update_position(self, delta_t:float):
		''' use a linear approximation or n_degree derivative to predict motion after some unit time. 
		A value of `delta_t=1` refers to moving 1 frame forward.
		'''
		self._position += self._velocity * delta_t
	
	def update_velocity(self, delta_t:float):
		self.velocity += self._acceleration * delta_t
	
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

	def get_hex_colour(self):
		return self.health_status.value
	def get_rgb_colour(self):
		rgb = self.health_status.value.convert_hex_to_rgb()
		return rgb.red, rgb.green, rgb.blue

	def set_colour(self):
		...