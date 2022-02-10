import argparse
import glob
from PIL import Image
import os

from merger import Merger
from reconstructor import Reconstructor


def get_img_list(path):
	return glob.glob(path + "/" + "person-*/*.png")


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
		pil_img.save("average_image/average_image.png")


def reconstruct_images(test_path, out_path):
	test_files = get_img_list(test_path)

	img_shape = (116, 120)  # cols, rows
	reconstructor = Reconstructor(img_shape)

	for infile in test_files:
		try:
			with Image.open(infile) as im:
				if im.mode != "L":
					print("Expected 8-bit pixels, black and white image. Exiting...")
					exit(1)
				reconstructed_img = reconstructor.process_img(im)

				path = out_path + "/" + infile.split("/")[-2]
				os.makedirs(path) if not os.path.exists(path) else None
				reconstructed_img.save(path + "/" + infile.split("/")[-1])
		except OSError:
			pass



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Reconstruct missing parts on depth images of '
												 'human faces. Run training or inference.')

	parser.add_argument('run_type',
						choices=["train", "test"],
						help='equals to test or train')

	parser.add_argument('path',
						help='path to train or test dataset')

	parser.add_argument('--out',
						help='output directory for inference results',
						default="dataset/reconstructed")
	args = parser.parse_args()

	if args.run_type == "train":
		create_average_image(args.path)
	else:
		reconstruct_images(args.path, args.out)
