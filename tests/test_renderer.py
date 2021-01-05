import os

import pytest

import renderer

class TestRenderer():
    TMP_BMP_FILE = "tmp.bmp"

    def teardown_method(self, method):
        if os.path.isfile(self.TMP_BMP_FILE):
            os.remove(self.TMP_BMP_FILE)

    def test_render_char_body_file_error(self):
        rend = renderer.Renderer()

        with pytest.raises(FileNotFoundError, match=r"Body sprite file bin/bad_file.spr is not found"):
            rend.render_char("bin/bad_file.spr", "bin/head.spr", "out_file_path.bmp")

    def test_render_char_head_file_error(self):
        rend = renderer.Renderer()

        with pytest.raises(FileNotFoundError, match=r"Head sprite file bin/bad_file.spr is not found"):
            rend.render_char("bin/taekwon.spr", "bin/bad_file.spr", "out_file_path.bmp")

    def test_render_char(self):
        rend = renderer.Renderer()
        rend.render_char("bin/taekwon.spr", "bin/head.spr", self.TMP_BMP_FILE)
