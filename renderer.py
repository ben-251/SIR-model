from backend import Blob, Colour, HealthStatus
from typing import List, Tuple
import random

class Universe:
	ticks:int
	blobs:List[Blob]
	size:Tuple[int,int]

	def __init__(self) -> None:
		self.size = 100,100

	def generate_blobs(self, n:int):
		for i in range(n):
			x,y = random.uniform(0,self.size[0]), random.uniform(0,self.size[1])
			self.blobs.append(Blob(initial_position=(x,y),id=i))
