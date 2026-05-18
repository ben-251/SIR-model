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

	def __init__(self, initial_position:Tuple[float,float], ID:int, health_status:Optional[HealthStatus]=None,time_sick:Optional[int]=None) -> None:
		if health_status is None:
			health_status = HealthStatus.SUSCEPTIBLE

		self.id = ID
		self._position = np.array(initial_position)
		self._velocity = np.zeros_like(self._position)
		self.health_status = health_status
		self.time_sick = 0 if time_sick is None else time_sick
	
	def get_position(self) -> np.ndarray: return self._position
	def get_velocity(self) -> np.ndarray: return self._velocity
	def set_position(self, position:Tuple[float,float]): self._position = np.array(position)
	def set_velocity(self, velocity:Tuple[float,float]): self._velocity = np.array(velocity)

	def get_hex_colour(self):
		return self.health_status.value
	def get_rgb_colour(self):
		rgb = self.health_status.value.convert_hex_to_rgb()
		return rgb.red, rgb.green, rgb.blue

	def set_colour(self):
		...