from nodes import *


class Sprite:
    def __init__(self, parent=None, texture=None, size=None, colour=(0, 0, 0)):
        self.colour = colour
        if texture:
            self.texture = texture
        elif size:
            texture = pygame.Surface(size)
            texture.fill(self.colour)
            self.texture = Texture(texture)
        else:
            raise Exception("size not given")
        parent.add_child(self)

        self.position = (0, 0)
        self.rect = self.texture.image.get_rect()
        self.rect.topleft = (0, 0)
        self.anchor_point = (0.5, 0.5)
        self.parent = parent
        self.children = []
        self.rotation = 0.0  # rads

    def draw(self):
        pos = self.rect
        pos.x = -pos.w * self.anchor_point[0]
        pos.x += self.position[0]
        pos.y = -pos.h * self.anchor_point[1]
        pos.y += self.position[1]
        self.parent.screen.blit(self.texture.image, pos)


class Texture:
    def __init__(self, image):
        if isinstance(image, pygame.Surface):
            self.image = image
        else:
            self.image = pygame.image.load(image)

    def subtexture(self, rect):
        return Texture(self.image.subsurface(rect))


class Action:  # TODO make action class and implement it into nodes
    def __init__(self):
        pass


"""test overrides"""
