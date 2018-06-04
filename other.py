from pygame import Surface, image
from scene.geometry import Point

class Texture:
    def __init__(self, im=None):
        if isinstance(im, Surface):
            self.image = im
        elif im:
            self.image = image.load(im)
        else:
            self.image = Surface((0, 0))
        self.original = self.image
        self.filtering_mode = 0  # todo implement and add constants
        self.size = 0  # todo add geter

    def subtexture(self, rect):

        rect2 = self.original.get_rect()

        return Texture(self.original.subsurface(
            ((rect[0]) * rect2[2], (1 - rect[1] - rect[3]) * rect2[3], rect[2] * rect2[2], rect[3] * rect2[3])))


class Action:  # TODO make action class and implement it into nodes
    def __init__(self):
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
