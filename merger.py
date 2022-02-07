import numpy as np


class Merger():
	def __init__(self):
		self.img_idx = 0
		self.average_image = np.full((120, 116), 255, dtype=np.uint)
		self.batch_size = 1
		self.sum_image = np.zeros_like(self.average_image)

	def apply_average(self):
		"""
		Average pixels on current image
		:return: write average image where non-white pixels are averaged
		"""
		nonzero_values_ids = np.where(self.sum_image < 255)
		# nonzero values of current image
		cur_nonzero = self.sum_image[nonzero_values_ids]
		# the corresponding values on average image
		av_nonzero = self.average_image[nonzero_values_ids]
		averaged_pixels = 0.5 * (av_nonzero + cur_nonzero / self.batch_size)

		# paste pixels on original image
		self.average_image[nonzero_values_ids] = averaged_pixels
		self.average_image.astype(np.uint8)

	def merge_to_one(self, image):
		self.sum_image += np.asarray(image)
		print(np.asarray(image)[0,0], image.getpixel((0,0)))
		if self.img_idx % self.batch_size == 0:
			self.apply_average()
			self.sum_image = np.zeros_like(self.average_image)
		self.img_idx += 1
		return self.average_image