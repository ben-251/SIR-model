from backend import Blob, Colour, HealthStatus
from typing import Dict, List, Tuple, Optional
from PIL import Image as Im
from PIL import ImageDraw
import random
import cv2 
import math

class TargetNotFoundError(Exception): ...

class Frame:
	render: Optional[str|Im.Image] = None
	
	def __init__(self, blobs:List[Blob]=[]) -> None:
		self.blobs = blobs

	def find_blob(self,blob_id:int):
		for blob in self.blobs:
			if blob.id == blob_id:
				return blob
		raise TargetNotFoundError()

	def update_blob(self, blob_id:int, **kwargs):
		try:
			blob = self.find_blob(blob_id)
		except TargetNotFoundError:
			print(f"Blob No.{blob_id} does not exist. Skipping...")
			return None


		for property_name,value in kwargs.items():
			# check if private. if so, then call setter.
			if property_name.startswith("_"):
				setter = getattr(blob, f"set{property_name}")
				setter(value)
			else:
				setattr(blob, property_name, value) 

	def store_blobs(self, *blobs:Blob):
		for blob in blobs:
			self.blobs.append(blob)



	

class Universe:
	ticks:int
	blobs:List[Blob]
	size:Tuple[int,int]
	frames:Dict[int, Im.Image]

	def __init__(self, size:Optional[Tuple[int,int]]=None, blob_count:int=25, health_ratio:Tuple[int,int,int, int]=(1,0,0,0)) -> None:
		self.size = 100,100
		self.ticks = 0
		self.generate_blobs(blob_count, health_ratio)

	def generate_health_pattern(self, n:int, health_ratio):
		pattern = []
		micro_count = math.ceil(n/sum(health_ratio))
		for proportion, health_stat in zip(health_ratio, HealthStatus):
			number_to_add = micro_count * proportion
			pattern.extend([health_stat]*number_to_add) # at this point it's SSSSSSSSIIIIIIRRDDDDDDDD for example
		random.shuffle(pattern)

		# remove any excess numbers until pattern is correct size
		return pattern[:n]

	def generate_blobs(self, n:int, health_ratio:Optional[Tuple[int,int,int,int]]=None):
		self.blobs = []
		health_pattern = self.generate_health_pattern(n, health_ratio)
		for i in range(n):
			x,y = random.uniform(0,self.size[0]), random.uniform(0,self.size[1])
			health = health_pattern[i]
			self.blobs.append(Blob(initial_position=(x,y),ID=i,health_status=health))

	def initialise_frame(self):
		'''
		Shows all blobs in the real plane.
		Opens up a frame to animate blobs on according to their individual physical properties.
		'''

	def render_next_frame(self) -> Im.Image:
		new_image = Im.new(mode='RGB', size=self.size)
		...
		return new_image

	def update_physics(self):
		for blob in self.blobs:
			blob.update_acceleration(self.ticks)
			blob.update_velocity(1)
			blob.update_position(1)

	def generate_frames(self,end_frame:Optional[int]=None):
		end_frame = 10_000 if end_frame is None else end_frame

		while self.ticks < end_frame:
			self.update_physics()
			yield self.render_next_frame()
			self.ticks += 1
	
	def generate_video(self,end_frame:Optional[int]=None):
		frames = list(self.generate_frames(end_frame))
		import numpy as np
		dimensions = (frames[0].size)
		format_ = cv2.VideoWriter_fourcc(*"mp4v")
		FPS = 30
		video = cv2.VideoWriter('output.mp4', format_, FPS, dimensions)

		for i, frame in enumerate(frames):
			print( f'Done: {round(i * 100 / len(frames), 1)} % - {frame}', end="\r") # \r makes it overwrite
			video.write(cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))
		video.release()


universe = Universe()