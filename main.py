from renderer import Universe

def main():
	world = Universe(blob_count=5)
	world.generate_video()


if __name__ == "__main__":
	main()