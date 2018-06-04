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


class Sceneold:  # an experiment scene class
    def __init__(self, size=None, title="window"):
        pygame.init()

        if size:
            self.size = size
        else:
            self.size = get_screen_size()

        self.tee = Tee(self)
        self.title = title
        self.running = True
        self.bg = (0, 0, 0)
        self.children = []

        pygame.display.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)

        self.bounds = get_bounds(pygame.display.get_wm_info()["window"])
        # all done, call setup
        self.setup()

    def add_child(self, kid):
        self.children.append(kid)

    def draw(self):
        for i in self.children:
            i.draw()

    def present(self):
        while self.running:
            self.screen.fill(self.bg)
            self.tee.loop(pygame.event.get())
            self.update()
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def _quit(self):
        self.running = False

    def quit(self):
        pass

    def setup(self):
        pass

    def update(self):
        pass

    def touch_began(self, touch):
        pass

    def touch_moved(self, touch):
        pass

    def touch_ended(self, touch):
        pass


"""test overrides"""
