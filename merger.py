import numpy as np


class Merger:
	def __init__(self, shape, batch):
		self.img_idx = 0
		self.average_image = None
		self.batch_size = batch
		self.sum_image = np.zeros(shape[::-1], dtype=np.uint)

	def apply_average(self):
		"""
		Average pixels on image batch. Only non-white pixels are averaged
		:return: None
		"""
		if self.average_image is None:
			self.average_image = self.sum_image

		nonzero_values_ids = np.where(self.sum_image < 255)
		# nonzero values of current image
		cur_nonzero = self.sum_image[nonzero_values_ids]
		# the corresponding values on average image
		av_nonzero = self.average_image[nonzero_values_ids]
		averaged_pixels = 0.5 * (av_nonzero + cur_nonzero / self.batch_size)

		# paste pixels on original image
		self.average_image[nonzero_values_ids] = averaged_pixels
		self.average_image = self.average_image.astype(np.uint8)

	def merge_to_one(self, image):
		"""
		Merge current image to previous in batch.
		:param image: current input image
		:return: numpy array of the same size with averaged pixels
		"""
		self.sum_image += np.asarray(image)
		if self.img_idx % self.batch_size == 0:
			self.apply_average()
			self.sum_image.fill(0)
		self.img_idx += 1
		return self.average_image