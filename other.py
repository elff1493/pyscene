from pygame import Surface


class Texture:
    def __init__(self, image):
        if isinstance(image, Surface):
            self.image = image
        else:
            self.image = image.load(image)

    def subtexture(self, rect):
        return Texture(self.image.subsurface(rect))


class Action:  # TODO make action class and implement it into nodes
    def __init__(self):
        pass
