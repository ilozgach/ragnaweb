import pytest
import time

import char_image_cache
import entity


class TestCharImageCache:
    BASE_PATH = ""

    def test_constructor_no_entry_timeout(self):
        cache = char_image_cache.CharImageCache(self.BASE_PATH)

        assert cache.base_path == self.BASE_PATH
        assert cache.entry_timeout == char_image_cache.CharImageCache.DEFAULT_ENTRY_TIMEOUT

    def test_constructor_with_entry_timeout(self):
        cache = char_image_cache.CharImageCache(self.BASE_PATH, entry_timeout=20)

        assert cache.base_path == self.BASE_PATH
        assert cache.entry_timeout == 20

    def test_contains_empty(self):
        cache = char_image_cache.CharImageCache(self.BASE_PATH)
        char = entity.Char()

        assert char not in cache
        str

    def test_setitem_key_type_error(self):
        cache = char_image_cache.CharImageCache(self.BASE_PATH)

        with pytest.raises(TypeError, match=r"Invalid key type <class 'int'>"):
            cache[1] = ""

    def test_setitem_value_type_error(self):
        cache = char_image_cache.CharImageCache(self.BASE_PATH)
        char = entity.Char()

        with pytest.raises(TypeError, match=r"Invalid value type <class 'int'>"):
            cache[char] = 1

    def test_setitem(self):
        cache = char_image_cache.CharImageCache(self.BASE_PATH)
        char = entity.Char()

        cache[char] = "blah"

        assert cache.cache[char.char_id].char == char
        assert cache.cache[char.char_id].timestamp is not None
        assert cache.cache[char.char_id].image_path == "blah"

    def test_getitem_empty(self):
        cache = char_image_cache.CharImageCache(self.BASE_PATH)
        char = entity.Char()

        with pytest.raises(KeyError, match=r"Character with char_id None is not in the cache"):
            cache[char]

    def test_getitem_key_type_error(self):
        cache = char_image_cache.CharImageCache(self.BASE_PATH)

        with pytest.raises(TypeError, match=r"Invalid key type <class 'int'>"):
            cache[1]

    def test_getitem(self):
        cache = char_image_cache.CharImageCache(self.BASE_PATH)
        char = entity.Char()
        cache[char] = "blah"

        assert cache[char] == "blah"

    def test_entry_timeout(self):
        cache = char_image_cache.CharImageCache(self.BASE_PATH, entry_timeout=0.5)
        char = entity.Char()

        cache[char] = "blah"
        assert char in cache
        time.sleep(0.55)
        assert char not in cache

    def test_online(self):
        cache = char_image_cache.CharImageCache(self.BASE_PATH)
        char = entity.Char()
        char.online = False

        cache[char] = "blah"
        assert char in cache

        char.online = True
        assert char not in cache

