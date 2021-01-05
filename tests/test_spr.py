import filecmp
import os

import pygrf

class TestSpr():

	TMP_BMP_FILE = "tmp.bmp"

	def teardown_method(self, method):
		if os.path.isfile(self.TMP_BMP_FILE):
			os.remove(self.TMP_BMP_FILE)

	def test_read_spr_file(self):
		spr = pygrf.open_spr("bin/frus.spr")
		assert len(spr) == 42

		pil_image = spr[0].to_pil_image()
		pil_image.save(self.TMP_BMP_FILE)
