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