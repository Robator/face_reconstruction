import numpy as np


class Merger:
	def __init__(self, shape, batch):
		self.img_idx = 0
		self.average_image = None
		self.batch_size = batch
		self.sum_image = np.zeros(shape[::-1], dtype=np.uint)

	def find_intersection_by_ids(self, xy1: tuple):
		"""
		Find intersection between given array with x and y coordinates and
		coordinates of average image which are not equal 255
		:param xy1: x and y indices
		:return: intersection mask
		"""
		xy2 = np.where(self.average_image < 255)

		x_mask = np.zeros_like(xy1[0], dtype=bool)
		y_mask = np.zeros_like(x_mask)
		i = 0
		for x1, x2 in zip(xy1[0], xy2[0]):
			x_mask[i] = (x1 == x2)
			i += 1
		i = 0
		for y1, y2 in zip(xy1[1], xy2[1]):
			y_mask[i] = (y1 == y2)
			i += 1
		mask = (x_mask & y_mask)
		return mask

	def apply_average(self):
		"""
		Average pixels on intersection of current batch and average image.
		Only non-white pixels are averaged
		"""
		if self.average_image is None:
			self.average_image = self.sum_image

		nonwhite_px_ids = np.where(self.sum_image < 255)

		# apply mask
		intersection_mask = self.find_intersection_by_ids(nonwhite_px_ids)
		nonwhite_px_ids_x, nonwhite_px_ids_y = nonwhite_px_ids
		nonwhite_px_ids_x = nonwhite_px_ids_x[intersection_mask]
		nonwhite_px_ids_y = nonwhite_px_ids_y[intersection_mask]
		nonwhite_px_ids = (nonwhite_px_ids_x, nonwhite_px_ids_y)

		# take chosen values of current image
		cur_nonwhite = self.sum_image[nonwhite_px_ids]
		# and values with corresponding indices on average image
		av_nonwhite_px = self.average_image[nonwhite_px_ids]
		averaged_pixels = 0.5 * (av_nonwhite_px + cur_nonwhite / self.batch_size)

		# save average image in memory for next call
		self.average_image[nonwhite_px_ids] = averaged_pixels
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
