function parseSpr(d) {
    palette = d.slice(d.length - 1024)

    var b = 4
    var nof_frames = d[b] | d[b + 1] << 8

    b += 4
    var images = []

    var i = 0
    for (i = 0; i < nof_frames; i++) {
        var width = d[b] | d[b + 1] << 8
        var height = d[b + 2] | d[b + 3] << 8
        var comp_len = d[b + 4] | d[b + 5] << 8

        var extra = 4 - width % 4
        if (extra == 4) {
            extra = 0
        }

        var buf = []

        var j = 0
        while (j < comp_len) {
            if (d[b + 6 + j] == 0) {
                j += 1

                var k = 0
                for (k = 0; k < d[b + 6 + j]; k++) {
                    buf.push(0x00)
                }
            }
            else {
                buf.push(d[b + 6 + j])
            }
            j += 1
        }

        j = 0
        var pixels = []
        while (j < buf.length) {
            if (extra > 0) {
                var k = 0
                for (k = 0; k < extra; k++) {
                    pixels.splice(0, 0, 0x00)
                }
            }

            pixels.splice.apply(pixels, [0, 0].concat(buf.slice(j, j + width)))
            j += width
        }

        images.push([width, height, pixels])
        b += comp_len + 6
    }

    return [images, palette]
}

function as_signed_4byte_int(val) {
    var mul = 1
    if (val & (0x1 << 31)) {
        mul = -1
    }

    if (mul > 0) {
        return val & 0x7fffffff
    } else {
        return (0x7fffffff - (val & 0x7fffffff) + 1) * mul
    }
}

function parseAct(d) {
    var actions = []

    var header = d[0] | d[1] << 8
    var version_minor = d[2]
    var version_major = d[3]

    actions = []
    var nactions = d[4] | d[5] << 8
    b = 16

    for (var iaction = 0; iaction < nactions; iaction++) {
        var sprites = []
        var nsprites = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
        b += 4

        for (var isprite = 0; isprite < nsprites; isprite++) {
            var tmp_sprite = []
            var frames = []

            b += 32
            var nframes = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
            b += 4

            for (var iframe = 0; iframe < nframes; iframe++) {
                var tmp_frame = []
                var offset_x = as_signed_4byte_int(d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24)
                b += 4
                var offset_y = as_signed_4byte_int(d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24)
                b += 4
                var image = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                b += 4
                var direction = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                b += 4

                tmp_frame.push(offset_x)
                tmp_frame.push(offset_y)
                tmp_frame.push(image)
                tmp_frame.push(direction)

                if (version_major >= 2) {
                    var color = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                    b += 4
                    var scale_x = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                    b += 4

                    var scale_y = scale_x
                    if (version_major > 2 || (version_major == 2 && version_minor >= 4)) {
                        var scale_y = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4
                    }

                    var rotation = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                    b += 4
                    var sprite_type = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                    b += 4

                    tmp_frame.push(color)
                    tmp_frame.push(scale_x)
                    tmp_frame.push(scale_y)
                    tmp_frame.push(rotation)
                    tmp_frame.push(sprite_type)

                    if (version_major > 2 || (version_major == 2 && version_minor >= 5)) {
                        size_x = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4
                        size_y = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4

                        tmp_frame.push(size_x)
                        tmp_frame.push(size_y)
                    }
                }

                frames.push(tmp_frame)
            }

            tmp_sprite.push(frames)

            if (version_major >= 2) {
                var event_index = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                tmp_sprite.push(event_index)
                b += 4
                if (version_major > 2 || (version_major == 2 && version_minor >= 3)) {
                    pivots = []
                    var npivots = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                    b += 4

                    for (var ipivot = 0; ipivot < npivots; ipivot++) {
                        pivot_unknown = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4
                        pivot_center_x = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4
                        pivot_center_y = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4
                        pivot_attribute = d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24
                        b += 4

                        pivots.push([pivot_unknown, pivot_center_x, pivot_center_y, pivot_attribute])
                    }

                    tmp_sprite.push(pivots)
                }
            }

            sprites.push(tmp_sprite)
        }

        actions.push(sprites)
    }

    return actions
}