import numpy as np
import sys
from PIL import Image
import glob

average_image = np.zeros((120, 116), dtype = np.int)
sum_image = np.zeros_like(average_image)
batch_size = 1

train_path = "./db_dep/train/"
train_files = glob.glob(train_path + "person-*/*.png")

def merge_to_one(image, img_idx):
	global sum_image, average_image
	if img_idx == 0:
		average_image = np.zeros_like(average_image)
	sum_image += np.asarray(image)
	print(np.asarray(image)[0, 0], image.getpixel((0, 0)))
	if img_idx % batch_size == 0:
		average_image = 0.5 * (average_image + sum_image / batch_size)
		average_image = average_image.astype(int)
		print("element (0,0):", average_image[0, 0])
		sum_image = np.zeros_like(average_image)
	return average_image


img_idx = 0
for infile in train_files:
	try:
		with Image.open(infile) as im:
			if im.mode != "L":
				print("Expected 8-bit pixels, black and white image. Exiting...")
				exit(1)
			print(infile, im.format, f"{im.size}x{im.mode}")
			av_img = merge_to_one(im, img_idx)
			new_img = Image.fromarray(av_img, mode="L")
			img_idx += 1
	except OSError:
		pass

img1 = Image.new("L", (116, 120), "white")
img2 = Image.new("L", (116, 120), "black")
av_img = merge_to_one(img1, 0)
print(av_img)
av_img = merge_to_one(img2, 1)
print(av_img)
av_img = merge_to_one(img1, 2)
print(av_img)