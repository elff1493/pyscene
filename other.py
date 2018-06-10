import os

import PIL
from pygame import Surface
from pygame import image
from scene.geometry import Point

builtins = os.listdir("scene/Media")
print(builtins)


class Texture:
    def __init__(self, im=None):  # todo clean up, it a mess
        if isinstance(im, Surface):
            self.image = im
        elif isinstance(im, str):
            for start in builtins:
                if im.startswith(start + ":"):
                    for file in os.listdir("scene/Media" + "/" + start):
                        if file.startswith(im[len(start) + 1:]):
                            im = "scene/Media/" + start + "/" + file
            self.image = image.load(im)
        elif isinstance(im, PIL.Image):
            self.image = image.fromstring(image.tostring(), image.size, image.mode)
        self.original = self.image

        self.filtering_mode = 0  # todo implement and add constants
        self.size = 0  # todo add geter

    def subtexture(self, rect):
        rect2 = self.original.get_rect()
        return Texture(self.original.subsurface(
            ((rect[0]) * rect2[2], (1 - rect[1] - rect[3]) * rect2[3], rect[2] * rect2[2], rect[3] * rect2[3])))


class Action:  # TODO make action class and implement it into nodes
    def __init__(self, **args):
        self._funk = self._call
        self._parent = None

    def _call(self):
        pass

    def _done(self):
        pass

    def _inter(self, p1, p2, t):
        return

    @classmethod
    def call(cls, func, duration=0.5):  # todo add
        pass

    @classmethod
    def fade_by(cls, alpha, duration=0.5, timing_mode=None):  # todo add # timeing mode
        pass

    @classmethod
    def fade_to(cls, alpha, duration=0.5, timing_mode=None):  # todo add
        pass

    @classmethod
    def group(cls, *actions):  # todo add
        pass

    @classmethod
    def move_by(cls, dx, dy, duration=0.5, timing_mode=None):  # todo add
        pass

    @classmethod
    def move_to(cls, x, y, duration=0.5, timing_mode=None):  # todo add
        pass

    @classmethod
    def repeat(cls, action, repeat_count):  # todo add
        pass

    @classmethod
    def rotate_by(cls, radians, duration=0.5, timing_mode=None):  # todo add
        pass

    @classmethod
    def rotate_to(cls, radians, duration=0.5, timing_mode=None):  # todo add
        pass

    @classmethod
    def scale_by(cls, scale, duration=0.5, timing_mode=None):  # todo add
        pass

    @classmethod
    def scale_to(cls, scale, duration=0.5, timing_mode=None):  # todo add
        pass

    @classmethod
    def scale_x_to(cls, scale, duration=0.5, timing_mode=None):  # todo add
        pass

    @classmethod
    def scale_y_to(cls, scale, duration=0.5, timing_mode=None):  # todo add
        pass

    @classmethod
    def set_uniform(cls, name, value, duration=0.5, timing_mode=None):  # todo add
        pass

    @classmethod
    def sequence(cls, *actions):  # todo add
        pass

    @classmethod
    def wait(cls, wait_duration):  # todo add
        pass


class Touch(object):
    def __init__(self, x, y, prev_x, prev_y, touch_id):
        self.touch_id = touch_id
        self.location = Point(x, y)
        self.prev_location = Point(prev_x, prev_y)
        self.layer = None

    def __eq__(self, other_touch):
        if not isinstance(other_touch, Touch):
            return False
        elif other_touch.touch_id == self.touch_id:
            return True
        return False

    def __hash__(self):
        return self.touch_id.__hash__()
