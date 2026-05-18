from backend import Blob, Colour, HealthStatus
from typing import Dict, List, Tuple, Optional
from itertools import product
import numpy as np
from PIL import Image as Im
from PIL import ImageDraw
import random
import cv2 
import math

class TargetNotFoundError(Exception): ...
class OutOfWorldError(Exception): ...

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
	'''
	The world of the creatures and epidemic.
	'''
	ticks:int
	blobs:List[Blob]
	size:Tuple[int,int]
	frames:Dict[int, Im.Image]

	def __init__(self, size:Optional[Tuple[int,int]]=None,
				blob_count:int=25, health_ratio:Tuple[int,int,int, int]=(1,0,0,0),
				recovery_rate:float=0.1, survival_rate:float=0.8, infection_rate = 0.08
			) -> None:
		self.size = 100,100
		self.ticks = 0
		self.generate_blobs(blob_count, health_ratio)
		self.recovery_rate = recovery_rate
		self.survival_rate = survival_rate
		self.infection_rate = infection_rate

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
			#TODO: for ~initialised-as-sick blobs~, set their infection duration to random length using the same function as below (generate_sickness_duration() or whatever)
	
	def search_for_nearby_blobs(self,target_blob:Blob,radius:int=3):
		target_position =target_blob.get_position()
		nearby_blobs = []

		for blob in self.blobs:
			if blob == target_blob: 
				continue
			other_position = blob.get_position()
			distance = np.linalg.norm(target_position - other_position)
			if distance <= radius:
				nearby_blobs.append(blob)
		
		return nearby_blobs

	def generate_sickness_duration(self) -> int:
		'''
		Chooses a random duration of infection according to a normal distribution.
		'''
		u = random.random()
		return math.floor(-math.log(u) / self.recovery_rate)
	
	def assign_fate(self) -> bool:
		'''
		Randomly assign a bool state describing whether the blob survives their disease.
		'''
		return random.random() < self.survival_rate
	
	def is_contracted(self) -> bool:
		return random.random() < self.infection_rate

	def update_healths(self):
		for blob in self.blobs:
			nearby_blobs = self.search_for_nearby_blobs(blob)
			if blob.health_status == HealthStatus.SUSCEPTIBLE and any(neighbour.health_status==HealthStatus.INFECTED for neighbour in nearby_blobs):
				#TODO: potentially make is_contracted take in the number of sick neighbours.
				isInfected = self.is_contracted()
				if isInfected:
					blob.health_status = HealthStatus.INFECTED
					blob.time_sick = self.generate_sickness_duration()
				continue
			elif blob.health_status == HealthStatus.INFECTED and blob.time_sick > 0:
				blob.time_sick -= 1
				continue
			elif blob.health_status == HealthStatus.INFECTED and blob.time_sick == 0:
				isCured = self.assign_fate()
				if isCured:
					blob.health_status = HealthStatus.RECOVERED
					continue
				else:
					blob.health_status = HealthStatus.DECEASED

	def create_frame(self, is_initial:Optional[bool]=False) -> Im.Image:
		'''
		Shows all blobs in the real plane.
		Opens up a frame to animate blobs on according to their individual physical properties.
		'''
		new_image = Im.new(mode='RGB', size=self.size, color=(255,230,155))
		draw = ImageDraw.Draw(new_image,  'RGBA')
		for blob in self.blobs:
			draw.circle(tuple(blob.get_position()),1,blob.get_rgb_colour())
		return new_image

	def render_next_frame(self) -> Im.Image:
		new_image = self.create_frame()
		return new_image

	def is_in_world(self, position:np.ndarray) -> bool:
		return 0 <=  position[0] and position[0] <= self.size[0] and 0 <= position[1] and position[1] <= self.size[1]

	def update_position(self, blob:Blob, delta_t:float) -> None:
		old_position = blob.get_position()
		new_position = old_position + blob.get_velocity() * delta_t
		if not self.is_in_world(new_position):
			raise OutOfWorldError()
		blob.set_position((new_position[0],new_position[1]))
	
	def update_velocity(self, blob, isRandom=False):
		if isRandom: 
			gamma = 0.8
		else: 
			gamma = 0.1
		
		current_velocity = blob.get_velocity()

		current_direction = math.atan2(current_velocity[1], current_velocity[0])
		noise = random.gauss(0,gamma)
		new_direction = current_direction + noise

		speed = np.linalg.norm(current_velocity)

		v_x =	speed * math.cos(new_direction)
		v_y =	speed * math.sin(new_direction)
		blob.set_velocity((v_x, v_y))

		
	def update_physics(self):
		for blob in self.blobs:
			try:
				self.update_velocity(blob)
				self.update_position(blob, 1)
			except OutOfWorldError:
				while True:
					self.update_velocity(blob,isRandom=True)
					self.update_position(blob, 1)
					continue

	def generate_frames(self,end_frame:Optional[int]=None):
		end_frame = 10_000 if end_frame is None else end_frame

		while self.ticks < end_frame:
			self.update_physics()
			self.update_healths()

			yield self.render_next_frame()

			self.ticks += 1
	
	def generate_video(self,end_frame:Optional[int]=None):
		frames = list(self.generate_frames(end_frame))

		dimensions = (frames[0].size)
		format_ = cv2.VideoWriter.fourcc(*"mp4v")
		FPS = 30
		video = cv2.VideoWriter('output.mp4', format_, FPS, dimensions)

		for i, frame in enumerate(frames):
			print( f'Progress: {round(i * 100 / len(frames), 1)} % - {frame}', end="\r") # \r makes it overwrite
			video.write(cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))
		video.release()


universe = Universe()