import os

def as_signed_4byte_int(val):
    mul = 1
    if val & (0x1 << 31):
        mul = -1
    if mul > 0:
        return val & 0x7fffffff
    else:
        return (0x7fffffff - (val & 0x7fffffff) + 1) * mul


def read_act(path):
    with open(path, "rb") as f:
        d = f.read()

    d = map(ord, d)

    header = d[0] | d[1] << 8
    version_minor = d[2]
    version_major = d[3]

    nactions = d[4] | d[5] << 8
    print "nactions", nactions
    b = 16

    for iaction in range(nactions):
        nsprites = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
        print "nsprites", nsprites
        b += 4
        for isprite in range(nsprites):
            b += 32
            nframes = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
            print "nframes", nframes
            b += 4
            for iframe in range(nframes):
                offset_x = as_signed_4byte_int(d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24)
                b += 4
                offset_y = as_signed_4byte_int(d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24)
                b += 4
                image = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                b += 4
                direction = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                b += 4
                if version_major >= 2:
                    color = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                    b += 4
                    scale_x = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                    b += 4
                    if version_major > 2 or (version_major == 2 and version_minor >= 4):
                        scale_y = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4
                    else:
                        scale_y = scale_x
                    rotation = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                    b += 4
                    sprite_type = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                    b += 4
                    if version_major > 2 or (version_major == 2 and version_minor >= 5):
                        size_x = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4
                        size_y = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4
            if version_major >= 2:
                event_index = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                b += 4
                if version_major > 2 or (version_major == 2 and version_minor >= 3):
                    npivots = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                    b += 4
                    for ipivot in range(npivots):
                        pivot_unknown = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4
                        pivot_center_x = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4
                        pivot_center_y = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4
                        pivot_attribute = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4


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

    # print d[len(d) - 1024:]
    palette = reverse_palette(d[len(d) - 1024:])
    # print palette

    b = 4
    nof_frames = d[b] | d[b + 1] << 8

    b += 4
    images = []
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

        images.append((width, height, pixels))

        # print "!!!", width, height, width * height, len(pixels)

        b += comp_len + 6

    width = images[0][0]
    height = images[0][1]
    print width
    print height
    print width * height
    print (width + width % 4) * height
    print len(images[0][2])
    for i in range(height):
        print images[0][2][i * width:(i + 1) * width] 
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

    b.extend(palette)
    b.extend(pixels)

    with open("tmp.bmp", "wb") as f:
        f.write(b)


# read_act("taekwon.act")
# images, palette = read_spr(os.path.join(os.path.dirname(os.path.abspath(__file__)), "taekwon.spr"))
# img_to_bmp(images[0][0], images[0][1], images[0][2], palette)
images, palette = read_spr("head.spr")