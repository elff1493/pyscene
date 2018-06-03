from pygame import Surface, image


class Texture:
    def __init__(self, im):
        if isinstance(im, Surface):
            self.image = im
        else:
            self.image = image.load(im)

    def subtexture(self, rect):
        return Texture(self.image.subsurface(rect))


class Action:  # TODO make action class and implement it into nodes
    def __init__(self):
        pass
