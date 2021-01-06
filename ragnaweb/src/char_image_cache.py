import entity
import timeit


class CharImageCacheEntry(object):
    def __init__(self, char, timestamp=None, image_path=None):
        self.char = char
        self.timestamp = timestamp or timeit.default_timer()
        self.image_path = image_path or str(char.char_id)


class CharImageCache(object):
    DEFAULT_ENTRY_TIMEOUT = 60 * 60 * 24  # 1 day

    def __init__(self, base_path, entry_timeout=None):
        self.base_path = base_path
        self.cache = {}
        self.entry_timeout = entry_timeout or self.DEFAULT_ENTRY_TIMEOUT

    def __contains__(self, item):
        if item.char_id in self.cache:
            if timeit.default_timer() > self.cache[item.char_id].timestamp + self.entry_timeout or \
                    item.online is True:
                del(self.cache[item.char_id])
                return False
            return True
        return False

    def __getitem__(self, key):
        if not type(key) == entity.Char:
            raise TypeError("Invalid key type {}".format(type(key)))
        if key.char_id not in self.cache:
            raise KeyError("Character with char_id {} is not in the cache".format(key.char_id))

        return self.cache[key.char_id].image_path

    def __setitem__(self, key, value):
        if not type(key) == entity.Char:
            raise TypeError("Invalid key type {}".format(type(key)))
        if not type(value) == str:
            raise TypeError("Invalid value type {}".format(type(value)))

        entry = CharImageCacheEntry(key, image_path=value)
        self.cache[key.char_id] = entry
