import glob
from PIL import Image
from merger import Merger
from reconstructor import Reconstructor


def get_img_list(path):
	return glob.glob(path + "person-*/*.png")


def create_average_image(train_path):
	train_files = get_img_list(train_path)

	img_shape = (116, 120)
	batch_size = 1
	merger = Merger(img_shape, batch_size)
	for infile in train_files:
		try:
			with Image.open(infile) as im:
				if im.mode != "L":
					print("Expected 8-bit pixels, black and white image. Exiting...")
					exit(1)
				av_img = merger.merge_to_one(im)
		except OSError:
			pass
	if len(train_files) > 0:
		pil_img = Image.fromarray(av_img, mode="L")
		pil_img.save("average_image.png")


def reconstruct_images(test_path):
	test_files = get_img_list(test_path)

	img_shape = (116, 120)  # cols, rows
	reconstructor = Reconstructor(img_shape, "average_image.png")

	for infile in test_files:
		try:
			with Image.open(infile) as im:
				if im.mode != "L":
					print("Expected 8-bit pixels, black and white image. Exiting...")
					exit(1)
				reconstructed_img = reconstructor.process_img(im)
				reconstructed_img.save("." + infile.split(".")[1] + "_reconstructed.png")
		except OSError:
			pass



if __name__ == "__main__":
	train = False
	train_path = "./db_dep/train/"
	test_path = "./db_dep/test/"

	if train:
		create_average_image(train_path)
	else:
		reconstruct_images(test_path)
