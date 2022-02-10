import unittest
from PIL import Image
import os

from reconstructor import Reconstructor


class TestReconstructor(unittest.TestCase):
	def test_get_symmetric_col(self):
		img_shape = (116, 120)  # cols, rows
		reconstructor = Reconstructor(img_shape, "average_image/average_image.png")
		res = reconstructor.get_symmetric_column(50)
		self.assertEqual(res, 65)

		res = reconstructor.get_symmetric_column(0)
		self.assertEqual(res, 115)

		res = reconstructor.get_symmetric_column(115)
		self.assertEqual(res, 0)

	def test_constructor(self):
		"""
		Test constructor and average image loading in rgb format
		"""
		img_shape = (116, 120)  # cols, rows

		img1 = Image.new("RGB", img_shape, "white")

		os.mkdir("average_image") if not os.path.exists("average_image") else None
		img1.save("average_image/average_image_test.png")

		reconstructor = Reconstructor(img_shape, "average_image/average_image_test.png")

		reconstructor = Reconstructor(img_shape, "somename")

		os.remove("average_image/average_image_test.png")

