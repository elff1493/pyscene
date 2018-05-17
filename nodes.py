import pygame

from other import Texture
from system import get_screen_size, get_bounds
from touch_event_engine import Tee


class SceneView:
    def __init__(self, size=None, name="window"):

        if size:
            self.size = size
        else:
            self.size = get_screen_size()

        self.tee = Tee(self)
        self.title = name
        self.running = True
        self.bg = (0, 0, 0)
        self.children = []
        self.screen = None
        self.bounds = get_bounds(pygame.display.get_wm_info()["window"])  # todo, is this 0,0,?

    def present(self):
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        self.bounds = get_bounds(pygame.display.get_wm_info()["window"])

    def _loop(self):
        while self.running:
            self.tee.loop(pygame.event.get())
            self.screen.fill(self.bg)
            self.update()
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def _quit(self):
        self.running = False


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


class Node:
    def __init__(self, position=(0, 0), z_position=0.0, scale=1.0,
                 x_scale=1.0, y_scale=1.0, alpha=1.0, speed=1.0, parent=None):
        # parameters
        self.position = position
        self.z_position = z_position
        self.scale = scale
        self.x_scale = x_scale
        self.y_scale = y_scale
        self._alpha = alpha
        self.speed = speed
        self.parent = parent
        # attributes
        # self.bbox
        # self._alpha
        # self.frame
        self.children = []
        # self.parent
        self.paused = False
        # self.position
        self.scene = False
        # self.speed
        # self.y_scale
        # self.z_position
        self.rotation = 0

    def _update_children(self):
        for kid in self.children:
            kid.update()

    @property
    def frame(self):  # TODO add bbox getter
        return self.position[0], self.position[1], 1, 1

    @property
    def bbox(self):  # TODO add bbox getter
        return None

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, alpha):
        self._alpha = alpha

    def add_child(self, node):
        self.children.append(node)

    def remove_from_parent(self):
        pass

    def remove_action(self, key):  # TODO add actions
        pass

    def remove_all_actions(self):  # TODO add actions
        pass

    def render_to_texture(self, crop_rect=None):
        if not crop_rect:
            crop_rect = self.frame
        return Texture(pygame.Surface())

    def point_to_scene(self, point):
        pass

    def point_from_scene(self, point):
        pass

    def run_action(self, action, key=""):  # TODO add actions
        pass


class EffectNode(Node):
    def __init__(self):
        pass


class SpriteNode(Node):  # TODO make better class
    def __init__(self):
        super().__init__()


class Scene(EffectNode):
    def __init__(self):
        super().__init__()

    def add_child(self, kid):  # TODO remove
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
