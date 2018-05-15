from scene import *
from touch_event_engine import RCLICK


class Test(Scene):
    def setup(self):
        # self.block = Block(self.screen, (2, 255, 230), 40, 40)
        self.ell = Sprite(parent=self, colour=(200, 100, 0), size=(100, 100), texture=Texture("image.png"))

    def update(self):
        pass
        # self.ell.position = pygame.mouse.get_pos()

    def touch_began(self, touch):
        if touch.touch_id == RCLICK:
            self.ell.position = touch.location

    def touch_moved(self, touch):
        if touch.touch_id == RCLICK:
            self.ell.position = touch.location


Test()
