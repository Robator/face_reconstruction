from PIL import Image
import numpy as np


class Reconstructor:
	def __init__(self, shape, av_img_name="average_image/average_image.png"):
		self.shape = shape
		self.avg_array = self.load_avg_image(av_img_name)

	def load_avg_image(self, av_img_name):
		"""
		Load average image
		:param av_img_name: path to average image
		:return: numpy array with average image or
			None if image is not found
		"""
		try:
			with Image.open(av_img_name) as im:
				if im.mode != "L":
					print("Expected 8-bit pixels, black and white image. Exiting...")
					return None
				return np.asarray(im)
		except FileNotFoundError:
			print(f"{av_img_name} is not found... Using only symmetry")
			return None

	def get_symmetric_column(self, cur_col):
		"""
		Calculate column number symmetrical to vertical center line
		:param cur_col: number of a column to find symmetrical value
		:return: symmetrical column number
		"""
		middle_even = (self.shape[0] - 1) / 2
		col = middle_even - (cur_col - middle_even)
		return int(col)

	def process_img(self, img):
		"""
		Reconstruct given image. Iterate over pixels and if one is equal to 255,
		try to replace it with the symmetrical one or from an average image
		:param img: pillow image
		:return: reconstructed png image
		"""
		img_array = np.asarray(img).copy()
		for col in range(self.shape[0]):
			for row in range(self.shape[1]):
				if img_array[row, col] != 255:
					continue
				symmetric_col = self.get_symmetric_column(col)
				if img_array[row, symmetric_col] != 255:
					img_array[row, col] = img_array[row, symmetric_col]
				elif self.avg_array is not None \
						and self.avg_array[row, col] != 255:
					img_array[row, col] = self.avg_array[row, col]

		return Image.fromarray(img_array, mode="L")
