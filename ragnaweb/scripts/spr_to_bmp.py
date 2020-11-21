import os
import numpy as np
from PIL import Image, ImageDraw


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

    actions = []
    nactions = d[4] | d[5] << 8
    b = 16

    for iaction in range(nactions):
        sprites = []
        nsprites = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
        b += 4

        for isprite in range(nsprites):
            tmp_sprite = []
            frames = []

            b += 32
            nframes = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
            b += 4

            for iframe in range(nframes):
                tmp_frame = []

                offset_x = as_signed_4byte_int(d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24)
                b += 4
                offset_y = as_signed_4byte_int(d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24)
                b += 4
                image = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                b += 4
                direction = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                b += 4

                tmp_frame.append(offset_x)
                tmp_frame.append(offset_y)
                tmp_frame.append(image)
                tmp_frame.append(direction)

                if version_major >= 2:
                    color = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                    b += 4
                    scale_x = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                    b += 4

                    scale_y = scale_x
                    if version_major > 2 or (version_major == 2 and version_minor >= 4):
                        scale_y = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4

                    rotation = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                    b += 4
                    sprite_type = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                    b += 4

                    tmp_frame.append(color)
                    tmp_frame.append(scale_x)
                    tmp_frame.append(scale_y)
                    tmp_frame.append(rotation)
                    tmp_frame.append(sprite_type)

                    if version_major > 2 or (version_major == 2 and version_minor >= 5):
                        size_x = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4
                        size_y = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4

                        tmp_frame.append(size_x)
                        tmp_frame.append(size_y)

                frames.append(tmp_frame)

            tmp_sprite.append(frames)

            if version_major >= 2:
                event_index = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                b += 4

                tmp_sprite.append(event_index)

                if version_major > 2 or (version_major == 2 and version_minor >= 3):
                    pivots = []
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

                        pivots.append([pivot_unknown, pivot_center_x, pivot_center_y, pivot_attribute])

                    tmp_sprite.append(pivots)
            sprites.append(tmp_sprite)
        actions.append(sprites)
    return actions


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
    # print width
    # print height
    # print width * height
    # print (width + width % 4) * height
    # print len(images[0][2])
    # for i in range(height):
    #     print images[0][2][i * width:(i + 1) * width]
    return images, palette


# def mix_body_and_head(body_width, body_height, body_pixels, body_palette, body_offset_x, body_offset_y, head_width, head_height, head_pixels, head_palette, head_offset_x, head_offset_y):

#     def get_x_y(i):
#         return p

#     char_pixels = []
#     char_palette = body_palette + head_palette

#     char_width = body_width
#     real_width = body_width + (4 - body_width % 4)
#     char_height = body_height // 2 + (body_offset_y - head_offset_y) + head_height // 2



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


def get_char_pixels():
    # body_width, body_height, body_pixels, body_palette, head_width, head_height, head_pixels, head_palette
    body_images, body_palette = read_spr(os.path.join(os.path.dirname(os.path.abspath(__file__)), "taekwon.spr"))
    head_images, head_palette = read_spr(os.path.join(os.path.dirname(os.path.abspath(__file__)), "head.spr"))
    head_actor_data = read_act(os.path.join(os.path.dirname(os.path.abspath(__file__)), "head.act"))

    body_width, body_height, body_pixels = body_images[0]

    head_frames = head_actor_data[0][0][0]
    for i, head_frame in enumerate(head_frames):
        if head_frame[2] >= 0:
            head_width, head_height, head_pixels = head_images[i]
            head_offset_x = head_frame[0]
            head_offset_y = head_frame[1]

    # char_width = body_width
    # char_height = body_height // 2 + abs(head_offset_y) + head_height // 2

    # def is_head(x, y):
    #     lx = (body_width // 2 + head_offset_x) - head_width // 2
    #     rx = (body_width // 2 + head_offset_x) + head_width // 2
    #     xpass = x >= lx and x <= rx

    #     ypass = y >= 0 and y < head_height

    #     if xpass and ypass:
    #         return (body_width // 2 + head_offset_x - head_width // 2, 0), (body_width // 2 + head_offset_x - head_width // 2 + head_width, 0)
    #     else:
    #         return None, None

    # def is_body(x, y):
    #     ish = is_head(x, y)
    #     if None in ish:
    #         xpass = x >= 0 and x < body_width
    #         ypass = y < head_height // 2 + head_of
    #     else:
    #         return None, None

    # import numpy as np
    # from PIL import Image

    def get_pil_image(width, height, pixels, palette):
        array = np.zeros([height, width, 4], dtype=np.uint8)
        y = height - 1
        while y >= 0:
            x = 0
            while x < width:
                p = (height - 1 - y) * (width + (4 - width % 4)) + x
                if (pixels[p] == 0):
                    x += 1
                    continue

                r = palette[pixels[p] * 4]
                g = palette[pixels[p] * 4 + 1]
                b = palette[pixels[p] * 4 + 2]
                a = 255

                array[y][x] = [b, g, r, a]

                x += 1
            y -= 1

        img = Image.fromarray(array)
        return img

    body_img = get_pil_image(body_width, body_height, body_pixels, body_palette)
    head_img = get_pil_image(head_width, head_height, head_pixels, head_palette)

    char_height = body_height
    if abs(head_offset_y) + head_height // 2 > body_height // 2:
        char_height = body_height // 2 + abs(head_offset_y) + head_height // 2
    char_img = Image.new("RGBA", (body_width, char_height), (255, 255, 255, 0))

    # draw = ImageDraw.Draw(char_img)
    # draw.bitmap(((10, 10)), head_img)

    print head_offset_x
    char_img.paste(head_img, (5, 5))

    char_img.save('testrgb.png')

# read_act("taekwon.act")
# images, palette = read_spr(os.path.join(os.path.dirname(os.path.abspath(__file__)), "taekwon.spr"))
# img_to_bmp(images[0][0], images[0][1], images[0][2], palette)
# images, palette = read_spr("head.spr")

get_char_pixels()
