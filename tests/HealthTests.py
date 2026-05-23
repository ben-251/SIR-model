from typing import Any
from renderer import Frame, TargetNotFoundError, Universe
from backend import Blob, HealthStatus
import bentests as bt 
import bentests.asserts as at

import numpy as np

class NeighbourRetrievalTests(bt.testGroup):
	def test_singleton(self):
		universe = Universe(expected_illness_duration=4,survival_rate=0,infection_rate=1)
		universe.blobs = [
			target := Blob((2,3),1)
		]
		neighbours = universe.search_for_nearby_blobs(target)
		at.assertEquals(
			neighbours,
			[]
		)
	def test_too_far_away(self):
		universe = Universe(expected_illness_duration=4,survival_rate=0,infection_rate=1)
		universe.blobs = [
			target := Blob((2,3),1),
			neighbour1 := Blob((45,23), 2)
		]
		neighbours = universe.search_for_nearby_blobs(target)
		at.assertEquals(
			neighbours,
			[]
		)

	def test_one_neighbour_barely_close_enough(self):
		universe = Universe(expected_illness_duration=4,survival_rate=0,infection_rate=1)
		universe.blobs = [
			target := Blob((2,3),1),
			neighbour1 := Blob((45,23), 2),
			neighbour2 := Blob((12,6), 2), # sqrt(10^2 + 3^2) ~ 10.4 < 11
		]
		neighbours = universe.search_for_nearby_blobs(target,radius=11)
		at.assertEquals(
			neighbours,
			[neighbour2]
		)

	def test_neighbour_on_radius(self): 
		universe = Universe(expected_illness_duration=4,survival_rate=0,infection_rate=1)
		universe.blobs = [
			target := Blob((2,3),1),
			neighbour1 := Blob((45,23), 2),
			neighbour2 := Blob((2,10), 2)
		]
		neighbours = universe.search_for_nearby_blobs(target,radius=7)
		at.assertEquals(
			neighbours,
			[neighbour2]
		)

class BlobColourTests(bt.testGroup):
	def test_sick_blob_rgb(self):
		universe = Universe(blob_count=2)
		colour = universe.blobs[0].get_rgb_colour()
		at.assertEquals(
			colour,
			(96, 168, 108)
		)
	



class S_to_I_Tests(bt.testGroup):
	def test_sick_neighbour(self):
		universe = Universe(expected_illness_duration=4,survival_rate=0,infection_rate=1)
		universe.blobs = [
			target := Blob((2,3),1,HealthStatus.SUSCEPTIBLE), # our target
			neighbour := Blob((2,5),2,HealthStatus.INFECTED) # a neighbour, 2 units away
		]
		universe.update_healths()

		at.assertEquals(
			target.health_status,
			HealthStatus.INFECTED
		)

	def test_sick_neighbour_with_immunity(self):
		universe = Universe(expected_illness_duration=4,survival_rate=0,infection_rate=0)
		universe.blobs = [
			target := Blob((2,3),1,HealthStatus.SUSCEPTIBLE), # our target
			neighbour := Blob((5,3),2,HealthStatus.INFECTED) # a neighbour, 5 units away
		]
		universe.update_healths()
		at.assertEquals(
			target.health_status,
			HealthStatus.SUSCEPTIBLE
		)

	def test_sick_blob_too_far(self):
		universe = Universe(expected_illness_duration=4,survival_rate=0,infection_rate=1)
		universe.blobs = [
			target := Blob((2,3),1,HealthStatus.SUSCEPTIBLE), # our target
			Blob((2,23),2,HealthStatus.INFECTED), # a neighbour, 20 units away
			Blob((2,23),3,HealthStatus.INFECTED) # a neighbour, 20 units away
		]
		universe.update_healths()
		at.assertEquals(
			target.health_status,
			HealthStatus.SUSCEPTIBLE
		)

class I_to_RD_Tests(bt.testGroup):
	def test_instant_death(self):
		universe = Universe(expected_illness_duration=0.001,survival_rate=0,infection_rate=1)
		universe.blobs = [
			Blob((2,3),1,HealthStatus.SUSCEPTIBLE),
			sick := Blob((2,5),2,HealthStatus.INFECTED)
		]
		universe.update_healths()
		at.assertEquals(
			sick.health_status,
			HealthStatus.DECEASED
		)

	def test_instant_cure(self):
		universe = Universe(expected_illness_duration=0.001,survival_rate=1,infection_rate=1)
		universe.blobs = [
			Blob((2,3),1,HealthStatus.SUSCEPTIBLE),
			sick := Blob((2,5),2,HealthStatus.INFECTED)
		]
		universe.update_healths()
		at.assertEquals(
			sick.health_status,
			HealthStatus.RECOVERED
		)

	def test_eventual_cure(self):
		universe = Universe(expected_illness_duration=56,survival_rate=1,infection_rate=1)
		universe.blobs = [
			Blob((2,3),1,HealthStatus.SUSCEPTIBLE),
			sick := Blob((2,5),2,HealthStatus.INFECTED)
		]

		for _ in range(70):
			universe.update_healths()
			universe.ticks += 1

		at.assertEquals(
			sick.health_status,
			HealthStatus.RECOVERED
		)

	def test_eventual_too_early_for_cure(self):
		universe = Universe(expected_illness_duration=56,survival_rate=1,infection_rate=1)
		universe.blobs = [
			Blob((2,3),1,HealthStatus.SUSCEPTIBLE),
			sick := Blob((2,5),2,HealthStatus.INFECTED)
		]

		sick.time_sick = universe.generate_sickness_duration()

		for _ in range(4):
			universe.update_healths()
			universe.ticks += 1

		at.assertEquals(
			sick.health_status,
			HealthStatus.INFECTED
		)