import struct


class Layer(object):
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.index = 0
        self.flags = 0


class Frame(object):
    def __init__(self):
        self.layers = []


class Animation(object):
    def __init__(self):
        self.frames = []


class Color(object):
    def __init__(self, val=0):
        self.r = (val & 0xff000000) >> 24
        self.g = (val & 0xff0000) >> 16
        self.b = (val & 0xff00) >> 8
        self.a = val & 0xff

    @staticmethod
    def from_rgba32(val):
    	c = Color()
        c.r = (val & 0xff000000) >> 24
        c.g = (val & 0xff0000) >> 16
        c.b = (val & 0xff00) >> 8
        c.a = val & 0xff
        return c

    def to_rgba32(self):
        red = self.r << 24
        green = self.g << 16
        blue = self.b << 8
        alpha = self.a
        return self.r << 24 | self.b << 16 | self.g << 8 | self.a


class Act(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.__read_act_file()

    def __read_act_file(self):
        with open(self.file_path, "rb") as f:
            # Read ACT file header:
            #    signature - 2 bytes, char
            #    version - 2 bytes, unsigned short
            #    actions count - 2 bytes, unsigned short
            #    padding - 10 bytes
            self.signature = f.read(2)
            self.version, = struct.unpack('<H', f.read(2))
            self.animations = []

            animations_count, = struct.unpack('<H', f.read(2))
            f.read(10)

            for ianimation in range(animations_count):
                # Read animations
                #    sprites count - 4 bytes, unsigned int

                animation = Animation()
                frames_count, = struct.unpack('<i', f.read(4))
                for iframe in range(frames_count):
                    # Read frames
                    #    unused - 32 bytes
                    #    layer count - 4 bytes, unsigned int

                    frame = Frame()
                    f.read(32)
                    layer_count, = struct.unpack('<i', f.read(4))

                    for ilayer in range(layer_count):
                        layer = Layer()

                        layer.offset_x, layer.offset_y, layer.index, layer.flags = struct.unpack('<iiII', f.read(16))
                        if self.version >= 0x200:
                            layer.color = Color(*struct.unpack('<I', f.read(4)))
                        if self.version >= 0x204:
                            layer.zoom, layer.zoom_y = struct.unpack('<ff', f.read(8))
                        elif self.version >= 0x200:
                            layer.zoom, = struct.unpack('<f', f.read(4))
                        if self.version >= 0x200:
                            layer.angle, = struct.unpack('<f', f.read(4))
                        if self.version >= 0x205:
                            f.read(12)
                        elif self.version >= 0x200:
                            f.read(4)

                        frame.layers.append(layer)

                        if self.version >= 0x200:
                            frame.trigger, = struct.unpack('<i', f.read(4))

                        if self.version >= 0x203:
                        	# Skip pivotss
                            count, = struct.unpack('<i', f.read(4))
                            f.read(16 * count)

                    animation.frames.append(frame)
                self.animations.append(animation)

            # TODO: parse triggers
            # TODO: parse intervals


