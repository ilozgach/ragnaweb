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


def read_spr(path):
    with open(path, "rb") as f:
        d = f.read()

    magic_header = d[0] + d[1] + d[2] + d[3]
    assert magic_header == "SP\001\002"

    d = map(ord, d)

    b = 4
    nof_frames = d[b] | d[b + 1] << 8

    b += 4
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

        print pixels

        from PIL import Image

        img = Image.new('RGB', (width, height))
        img.putdata(pixels)
        img.save('image.png')

        break

        b += comp_len + 6
        # break


# read_act("d:/frus.act")
read_spr("d:/frus.spr")
