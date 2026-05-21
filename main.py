from renderer import Universe

def main():
	world = Universe(health_ratio=(2,2,0,0), blob_count=5,
		expected_illness_duration=12, survival_rate=0.3, infection_rate=1)
	world.generate_video()
	# new_test = Universe(blob_count=6)
	# new_test.generate_frame_images(folder_path="output")


if __name__ == "__main__":
	main()