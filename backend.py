from enum import auto, Enum
from typing import Tuple, Optional
from numpy import linalg as ila
import numpy as np
import copy

class Colour(Enum):
	GREY = auto()
	BLUE = auto()
	RED = auto()
	GREEN = auto()

class HealthStatus(Enum):
	SUSCEPTIBLE = Colour.BLUE
	INFECTED = Colour.RED
	RECOVERED = Colour.GREEN
	DEAD = Colour.GREY

class Blob:
	_position:np.ndarray
	_velocity:np.ndarray
	_acceleration:np.ndarray

	def __init__(self, initial_position:Tuple[float,float], id:int, health_status:Optional[HealthStatus]=None) -> None:
		if health_status is None:
			health_status = HealthStatus.SUSCEPTIBLE

		self.position = np.array(initial_position)
		self.health_status = health_status

	def update_position(self, delta_t:float):
		# use a linear approximation or n_degree derivative to predict motion after t seconds
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
	
	def get_position(self):
		return self._position
	
	def get_velocity(self):
		return self._velocity
	
	def get_acceleration(self):
		return self._acceleration