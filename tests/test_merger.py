import unittest
from merger import Merger
from PIL import Image


class TestMerging(unittest.TestCase):
	def test_merging(self):
		merger = Merger()

		img1 = Image.new("L", (116, 120), "white")
		img1.putpixel((0, 0), 0)
		img2 = Image.new("L", (116, 120), "black")
		av_img = merger.merge_to_one(img1)
		self.assertEqual(av_img[0, 0], 127)
		self.assertEqual(av_img.shape, (120, 116))
		av_img = merger.merge_to_one(img2)
		self.assertEqual(av_img[0, 0], 63)
		av_img = merger.merge_to_one(img1)
		self.assertEqual(av_img[0, 0], 31)