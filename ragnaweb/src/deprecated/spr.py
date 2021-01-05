class Image(object):
	
	def __init__(self, width, height, pixels):
		self.width = width
		self.height = height
		self.pixels = pixels

	def to_raw_bitmap(self, palette):
	    b = bytearray()

	    def append_buf(val, byte_count):
	        for i in range(byte_count):
	            b.append((val >> (8 * i)) & 0xff)

	    offset = 54 + len(palette)
	    file_size = offset + len(self.pixels)
	    b.extend([ord("B"), ord("M")])
	    append_buf(file_size, 4)
	    append_buf(0, 4)
	    append_buf(offset, 4)

	    info_hsize = 40
	    append_buf(info_hsize, 4)

	    append_buf(self.width, 4)
	    append_buf(self.height, 4)

	    nof_planes = 1
	    append_buf(nof_planes, 2)

	    nof_bits = 8
	    append_buf(nof_bits, 2)

	    compression_type = 0
	    append_buf(compression_type, 4)

	    pixel_data_size = len(self.pixels)
	    append_buf(pixel_data_size, 4)

	    x_pixels_per_meter = 0
	    append_buf(x_pixels_per_meter, 4)

	    y_pixels_per_meter = 0
	    append_buf(y_pixels_per_meter, 4)

	    nof_colors = 256
	    append_buf(nof_colors, 4)

	    nof_important_colors = 0
	    append_buf(nof_important_colors, 4)

	    b.extend(palette)
	    b.extend(self.pixels)

	    return b


class Spr(object):

	def __init__(self, file_path):
		self.file_path = file_path
		self.__read_sprite_file()

	def __reverse_palette(self, palette):
	    res = []
	    for i in range(0, len(palette), 4):
	        res.append(palette[i + 2])
	        res.append(palette[i + 1])
	        res.append(palette[i])
	        res.append(0)
	    return res

	def __read_sprite_file(self):
	    with open(self.file_path, "rb") as f:
	        d = f.read()

	    magic_header = d[0] + d[1] + d[2] + d[3]
	    assert magic_header == "SP\001\002"

	    d = map(ord, d)

	    self.palette = self.__reverse_palette(d[len(d) - 1024:])

	    b = 4
	    nof_frames = d[b] | d[b + 1] << 8

	    b += 4
	    self.images = []
	    for i in range(nof_frames):
	        width = d[b] | d[b + 1] << 8
	        height = d[b + 2] | d[b + 3] << 8
	        comp_len = d[b + 4] | d[b + 5] << 8

	        i = 0
	        extra = 4 - width % 4
	        if extra == 4:
	            extra = 0
	        buf = []
	        while i < comp_len:
	            if d[b + 6 + i] == 0:
	                i += 1
	                buf.extend([0x00] * d[b + 6 + i])
	            else:
	                buf.extend([d[b + 6 + i]])
	            i += 1

	        i = 0
	        pixels = []
	        while i < len(buf):
	            if extra > 0:
	                pixels = [0x00] * extra + pixels
	            pixels = buf[i:i + width] + pixels
	            i += width

	        self.images.append(Image(width, height, pixels))

	        b += comp_len + 6
