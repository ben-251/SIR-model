from typing import Any
from renderer import Frame, TargetNotFoundError, Universe
from backend import Blob, HealthStatus, Colour
import bentests as bt 
import bentests.asserts as at
import numpy as np

class BlobGenerationTests(bt.testGroup):
	def test_all_healthy(self):
		universe = Universe(size=(100,100),blob_count=10,health_ratio=(1,0,0,0))
		at.assertEquals(
			list(blob.health_status for blob in universe.blobs),
			[HealthStatus.SUSCEPTIBLE]*10
		)

	#TODO: add more tests, like half-and-half, q and q and q and q, 1/3 and 1/3 and 1/3 and 0, etc
	
class AllEnumTests(bt.testGroup):
	def test_print_health(self, skip=True):
		# dummy test. obviously ridiculously annoying cuz i'll tweak the colours a bunch.
		output = str(HealthStatus.SUSCEPTIBLE)
		at.assertEquals(output,"\x1b[38;2;53;48;135mSUSCEPTIBLE\x1b[39m")

class FrameTests(bt.testGroup):
	def test_modify_blob_private(self):
		blob = Blob((0,0),1)
		frame = Frame(blobs=[blob])
		frame.update_blob(1,_position=(2,3))
		at.assertEquals(blob.get_position(),np.array((2,3)))

	def test_modify_blob_public(self):
		blob = Blob((0,0),1)
		frame = Frame(blobs=[blob])
		frame.update_blob(1,health_status=HealthStatus.INFECTED)
		at.assertEquals(blob.health_status,HealthStatus.INFECTED)
	
	def test_modify_blob_pub_and_pri(self):
		blob = Blob((0,0),1)
		frame = Frame(blobs=[blob])
		frame.update_blob(1,_position=(2,3))
		frame.update_blob(1,health_status=HealthStatus.INFECTED)
		at.assertEquals(
			(blob.health_status, list(blob.get_position())), #temporary bodge cuz bt can't compare that well on np yet
			(HealthStatus.INFECTED, list(np.array((2,3))))
		)	

	def test_not_found(self):
		with at.assertRaises(TargetNotFoundError):
			frame = Frame(blobs=[Blob((0,0),i) for i in range(5,10)])
			target_blob = frame.find_blob(1)
	
	def test_target_blob_matches_original(self):
		frame = Frame(blobs=[Blob((i,0),i) for i in range(5,10)])
		target_blob = frame.find_blob(6)
		bt.asserts.assertEquals(
			frame.blobs[1], # 5,6,7,8,9 -> blob 6 is the 2nd (1th) 
			target_blob
		)
	
	def test_modify_target_blob(self):
		frame = Frame(blobs=[Blob((i,0),i) for i in range(10)]) # 0 1 2 3 4 5 6 ...
		target_blob = frame.find_blob(5) # blob with id = 5 is the 6th one
		target_blob.set_position((50,30))
		at.assertEquals(
			frame.blobs[5].get_position(), # the 6th one
			np.array([50,30])
		)	


bt.test_all(
	BlobGenerationTests,
	FrameTests,
	AllEnumTests,
	stats_amount="high"
)