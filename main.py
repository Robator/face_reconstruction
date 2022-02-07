import glob
from PIL import Image
from merger import Merger

train_path = "./db_dep/train/"
train_files = glob.glob(train_path + "person-*/*.png")


def run():
	merger = Merger()
	for infile in train_files:
		try:
			with Image.open(infile) as im:
				if im.mode != "L":
					print("Expected 8-bit pixels, black and white image. Exiting...")
					exit(1)
				print(infile, im.format, f"{im.size}x{im.mode}")
				av_img = merger.merge_to_one(im)
				pil_img = Image.fromarray(av_img, mode="L")
		except OSError:
			pass