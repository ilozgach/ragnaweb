import os

def read_act(path):
    with open(path, "rb") as f:
        d = f.read()

    d = map(ord, d)

    header = d[0] << 8 | d[1]
    version = d[3]
    nanimations = d[5] << 8 | d[4]
    print "nanimations", nanimations
    for ianimation in range(nanimations):
        b = 13 + ianimation * 10
        nframes = d[b] << 24 | d[b + 1] << 16 | d[b + 2] << 8 | d[b + 3]
        print "nframes", nframes
        for iframe in range(nframes):
            bb = b + 32 + 4 + iframe * 10
            nsubframes = d[bb] << 24 | d[bb + 1] << 16 | d[bb + 2] << 8 | d[bb + 3]
            print "nsubframes", nsubframes
            for isubframe in nsubframes:
                # bbb = bb + 4 + 
                offset_x = d[bbb] << 24 | d[bbb + 1] << 16 | d[bbb + 2] << 8 | d[bbb + 3]
                offset_y = d[bbb + 4] << 24 | d[bbb + 5] << 16 | d[bbb + 6] << 8 | d[bbb + 7]
                image = d[bbb + 8] << 24 | d[bbb + 9] << 16 | d[bbb + 10] << 8 | d[bbb + 11]
                direction = d[bbb + 12] << 24 | d[bbb + 13] << 16 | d[bbb + 14] << 8 | d[bbb + 15]
                color = d[bbb + 16] << 24 | d[bbb + 17] << 16 | d[bbb + 18] << 8 | d[bbb + 19]
        break


def reverse_palette(palette):
    res = []
    for i in range(0, len(palette), 4):
        res.append(palette[i + 2])
        res.append(palette[i + 1])
        res.append(palette[i])
        res.append(0)
    return res


def read_spr(path):
    with open(path, "rb") as f:
        d = f.read()

    magic_header = d[0] + d[1] + d[2] + d[3]
    assert magic_header == "SP\001\002"

    d = map(ord, d)

    palette = reverse_palette(d[len(d) - 1024:])

    b = 4
    nof_frames = d[b] | d[b + 1] << 8

    b += 4
    images = []
    for i in range(nof_frames):
        width = d[b] | d[b + 1] << 8
        height = d[b + 2] | d[b + 3] << 8
        comp_len = d[b + 4] | d[b + 5] << 8

        print width, height, comp_len

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

        images.append((width, height, pixels))

        b += comp_len + 6

    return images, palette


def img_to_bmp(width, height, pixels, palette):
    b = bytearray()

    def append_buf(val, byte_count):
        for i in range(byte_count):
            b.append((val >> (8 * i)) & 0xff)

    offset = 54 + len(palette)
    file_size = offset + len(pixels)
    b.extend([ord("B"), ord("M")])
    append_buf(file_size, 4)
    append_buf(0, 4)
    append_buf(offset, 4)

    info_hsize = 40
    append_buf(info_hsize, 4)

    append_buf(width, 4)
    append_buf(height, 4)

    nof_planes = 1
    append_buf(nof_planes, 2)

    nof_bits = 8
    append_buf(nof_bits, 2)

    compression_type = 0
    append_buf(compression_type, 4)

    pixel_data_size = len(pixels)
    append_buf(pixel_data_size, 4)

    x_pixels_per_meter = 0
    append_buf(x_pixels_per_meter, 4)

    y_pixels_per_meter = 0
    append_buf(y_pixels_per_meter, 4)

    nof_colors = 256
    append_buf(nof_colors, 4)

    nof_important_colors = 0
    append_buf(nof_important_colors, 4)

    print hex(palette[0])
    print hex(palette[1])
    print hex(palette[2])
    print hex(palette[3])

    b.extend(palette)
    b.extend(pixels)

    with open("tmp.bmp", "wb") as f:
        f.write(b)


# read_act("d:/frus.act")
images, palette = read_spr(os.path.join(os.path.dirname(os.path.abspath(__file__)), "frus.spr"))
img_to_bmp(images[0][0], images[0][1], images[0][2], palette)
