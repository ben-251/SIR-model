import bentests as bt 

from tests.Initialisation import BlobGenerationTests, FrameTests, AllEnumTests
from tests.HealthTests import NeighbourRetrievalTests, I_to_RD_Tests, S_to_I_Tests

bt.test_all(
	BlobGenerationTests,FrameTests,AllEnumTests,
	NeighbourRetrievalTests,I_to_RD_Tests,S_to_I_Tests,
	skip_passes=True, stats_amount="low", nesting_output_depth=4
)
