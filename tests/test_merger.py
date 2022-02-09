import unittest
from PIL import Image
import numpy as np

from merger import Merger


class TestMerging(unittest.TestCase):
	def test_merging(self):
		"""
		Merge black and then white image with one changed pixel into
		white image with the same changed pixel
		"""
		img_shape = (116, 120)  # cols, rows
		batch_size = 1
		merger = Merger(img_shape, batch_size)
		pixel_value = 150

		img1 = Image.new("L", img_shape, "white")
		img1.putpixel((0, 0), pixel_value)
		img2 = Image.new("L", img_shape, "black")
		av_img = merger.merge_to_one(img1)
		self.assertEqual(av_img[0, 0], pixel_value)
		self.assertEqual(av_img.shape, img_shape[::-1])

		av_img = merger.merge_to_one(img2)
		self.assertEqual(av_img[0, 0], pixel_value / 2)

		av_img = merger.merge_to_one(img1)
		self.assertEqual(av_img[0, 0], int((pixel_value / 2 + pixel_value) / 2))

	def test_find_intersection_by_ids(self):
		"""
		Check output intersection mask is correct
		"""
		img_shape = (3, 1)  # cols, rows
		batch_size = 1
		merger = Merger(img_shape, batch_size)
		pixel_value = 0

		img1 = Image.new("L", img_shape, "white")
		img1.putpixel((0, 0), pixel_value)
		img1.putpixel((2, 0), pixel_value)
		arr2 = (np.array([0, 0]), np.array([0, 2]))
		av_img = merger.merge_to_one(img1)
		mask = merger.find_intersection_by_ids(arr2)

		self.assertTrue(np.all(mask == [True, True]))

	def test_intersection(self):
		"""
		Only matching pixels should be averaged. In this case after merging black image into
		white one only pixel at coordinate (0, 0) is changed
		"""
		img_shape = (116, 120)  # cols, rows
		batch_size = 1
		merger = Merger(img_shape, batch_size)
		pixel_value = 150

		img1 = Image.new("L", img_shape, "white")
		img1.putpixel((0, 0), pixel_value)
		img2 = Image.new("L", img_shape, "black")
		av_img = merger.merge_to_one(img1)
		av_img = merger.merge_to_one(img2)

		self.assertEqual(av_img[0, 0], 75)
		self.assertTrue(np.all(av_img[0:, 1:] == 255))