from renderer import Universe
from stats import plot_SIR_graph, survival_hypothesis_test

def main():
	world = Universe(size=(450,450), health_ratio=(70,1,0,0), blob_count=150, blob_size=4,
		expected_illness_duration=100, survival_rate=0.3, infection_rate=0.3)
	state_frames = list(world.generate_state_frames(end_frame=700))
	# plot_SIR_graph(state_frames)
	# world.generate_video(state_frames=state_frames)
	for rate in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]:
		print(rate, "reject" if survival_hypothesis_test(state_frames, rate, 0.05) else "fail to reject")


if __name__ == "__main__":
	main()