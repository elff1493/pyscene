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

        self.title = name
        self.running = True
        self.bg = (0, 0, 0)
        # self.children = []
        self.screen = None
        self.bounds = (0, 0)  # get_bounds(pygame.display.get_wm_info()["window"])  # todo, is this 0,0,?

        self.scene = None
        self.anti_alias = None
        self.frame_interval = None
        self.multi_touch_enabled = None
        self.shows_fps = None
        self.scene = None

        self.tee = None

    def present(self, orientations=None):
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        self.bounds = get_bounds(pygame.display.get_wm_info()["window"])

        # self.scene.view = self
        self.tee = Tee(self)
        self.scene.setup()
        self._loop()

    def _loop(self):
        while self.running:
            self.tee.loop(pygame.event.get())
            self.screen.fill(self.bg)
            self.scene.update()
            self.scene._update_children(self)
            pygame.display.flip()
        pygame.quit()

    def _quit(self):
        self.running = False


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
        self.parent = None
        if parent:
            parent.add_child(self)
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

    def _update_children(self, view):
        for kid in self.children:
            kid._update_children(view)

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
        node.parent = self
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
        super().__init__()


class SpriteNode(Node):  # TODO make better class
    def __init__(self, texture, position=(0, 0), z_position=0.0, scale=1.0,
                 x_scale=1.0, y_scale=1.0, alpha=1.0, speed=1.0, parent=None,
                 size=None, color='white', blend_mode=0
                 ):
        super().__init__(position=position, z_position=z_position, scale=scale,
                         x_scale=x_scale, y_scale=y_scale, alpha=alpha, speed=speed, parent=parent)

        self.color = color
        if texture:
            self.texture = texture
        elif size:
            texture = pygame.Surface(size)
            texture.fill(self.color)
            self.texture = Texture(texture)
        else:
            raise Exception("size not given")
        # parent.add_child(self)

        self.position = (0, 0)
        self.rect = self.texture.image.get_rect()
        self.rect.topleft = (0, 0)
        self.anchor_point = (0.5, 0.5)
        # self.parent = parent
        # self.children = []
        self.rotation = 0.0  # rads

    def _update_children(self, view):
        for kid in self.children:
            kid._update_children(view)
        pos = self.rect
        pos.x = -pos.w * self.anchor_point[0]
        pos.x += self.position[0]
        pos.y = -pos.h * self.anchor_point[1]
        pos.y += self.position[1]
        view.screen.blit(self.texture.image, pos)


class Scene(EffectNode):
    def __init__(self):
        super().__init__()

    def add_child(self, kid):  # TODO remove
        self.children.append(kid)

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
