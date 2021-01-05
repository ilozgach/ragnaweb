import os

import PIL.Image
import pygrf
import pygrf.graphics

class Renderer(object):

    def render_char(self, body_path, head_path, out_file_path):
        body_spr_path = body_path[:body_path.rfind(".")] + ".spr"
        body_act_path = body_path[:body_path.rfind(".")] + ".act"
        head_spr_path = head_path[:head_path.rfind(".")] + ".spr"
        head_act_path = head_path[:head_path.rfind(".")] + ".act"

        if not os.path.isfile(body_spr_path):
            raise FileNotFoundError("Body sprite file {} is not found".format(body_spr_path))
        if not os.path.isfile(body_spr_path):
            raise FileNotFoundError("Body act file {} is not found".format(body_act_path))
        if not os.path.isfile(head_spr_path):
            raise FileNotFoundError("Head sprite file {} is not found".format(head_spr_path))
        if not os.path.isfile(head_act_path):
            raise FileNotFoundError("Head act file {} is not found".format(head_act_path))

        # body_spr = pygrf.open_spr(body_spr_path)
        # body_image = body_spr[0]
        # body_pil_image = body_image.to_pil_image()
        # body_pil_image.putalpha(128)

        # head_spr = pygrf.open_spr(head_spr_path)
        # head_image = head_spr[0]
        # head_pil_image = head_image.to_pil_image()
        # head_pil_image.putalpha(128)

        # head_act = pygrf.open_act(head_act_path)

        # char_image = PIL.Image.new("RGBA", (body_image.width, body_image.height + head_image.height), (0, 0, 0, 0))

        # body_offset_x = 0
        # body_offset_y = 23
        # char_image.paste(body_pil_image, (body_offset_x, body_offset_y))

        # # head_offset_x = int((body_image.width - head_image.width) / 2.0) + head_act.animations[0].frames[0].layers[0].offset.x
        # head_offset_x = int((body_image.width - head_image.width) / 2.0)
        # head_offset_y = 0
        # char_image.paste(head_pil_image, (head_offset_x, head_offset_y))

        # char_image.save("char.bmp")

        body_spr = pygrf.open_spr(body_spr_path)
        body_image = body_spr[0]
        head_spr = pygrf.open_spr(head_spr_path)
        head_image = head_spr[0]
        head_act = pygrf.open_act(head_act_path)

        char_image_width = body_image.width
        char_image_height = head_image.height + body_image.height
        body_offset_x = 0
        body_offset_y = head_image.height - 6
        head_offset_x = int((body_image.width - head_image.width) / 2.0) - head_act.animations[0].frames[0].layers[0].offset.x
        head_offset_y = 0

        char_pixels = []
        for y in range(0, char_image_height):
            for x in range(0, char_image_width):
                char_pixel_color = pygrf.graphics.Color(0, 0, 0, 0)

                # is_this_head = False
                if x >= head_offset_x and x < head_offset_x + head_image.width and y >= head_offset_y and y < head_offset_y + head_image.height:
                    head_x = x - head_offset_x
                    head_y = y - head_offset_y
                    head_pixel_index = head_y * head_image.width + head_x
                    if head_image.data[head_pixel_index] != 0:  # Hack zero palette
                        char_pixels.append(head_image.pixels[head_pixel_index])
                        continue
                    # head_pixel_color = head_image.pixels[head_pixel_index]
                    # char_pixel_color = char_pixel_color.alpha_blend(head_pixel_color)

                if x >= body_offset_x and x < body_offset_x + body_image.width and y >= body_offset_y and y < body_offset_y + body_image.height:
                    body_x = x
                    body_y = y - body_offset_y
                    body_pixel_index = body_y * body_image.width + body_x
                    # body_pixel_color = body_image.pixels[body_pixel_index]
                    # char_pixel_color = char_pixel_color.alpha_blend(body_pixel_color)
                    char_pixels.append(body_image.pixels[body_pixel_index])
                    continue

                # char_pixels.append(char_pixel_color)
                char_pixels.append(pygrf.graphics.Color(0, 0, 0, 0))

        char_image = pygrf.graphics.Image(char_image_width, char_image_height, char_pixels, None, None)
        char_image.to_pil_image().save(out_file_path)