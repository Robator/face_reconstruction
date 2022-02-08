import unittest
from merger import Merger
from PIL import Image


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