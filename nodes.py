import pygame
from scene.geometry import Point, Rect
from scene.other import Texture
from scene.system import get_screen_size, get_bounds
from scene.touch_event_engine import Tee




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

        if self.scene.size:
            self.size = self.scene.size
        else:
            self.scene.size = Point(*self.size)

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
        self._position = Point(*position)
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
    def frame(self):
        return Rect(*self._position, 1, 1)

    @property
    def bbox(self):
        rec = self.frame
        for kid in self.children:
            rec = rec.union(kid.bbox)
        return rec

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, alpha):
        self._alpha = alpha

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = Point(*position)

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def remove_from_parent(self):
        self.parent.children.remove(self)  # todo test

    def remove_action(self, key):  # TODO add actions
        pass

    def remove_all_actions(self):  # TODO add actions
        pass

    def render_to_texture(self, crop_rect=None):
        if not crop_rect:
            crop_rect = self.frame
        return Texture(pygame.Surface())

    def point_to_scene(self, point):  # todo make recersive stuff
        if self.parent is Scene:
            pass
        else:
            new = self.parent.point_to_scene(point)
        return Point(2, 2)

    def point_from_scene(self, point):  # todo
        pass

    def run_action(self, action, key=""):  # TODO add actions
        pass


class EffectNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SpriteNode(Node):  # TODO make better class
    def __init__(self, texture=None, position=(0, 0), z_position=0.0, scale=1.0,
                 x_scale=1.0, y_scale=1.0, alpha=1.0, speed=1.0, parent=None,
                 size=None, color=(255, 255, 255), blend_mode=0
                 ):
        super().__init__(position=position, z_position=z_position, scale=scale,
                         x_scale=x_scale, y_scale=y_scale, alpha=alpha, speed=speed, parent=parent)

        self.color = color
        if texture:
            self.texture = texture
        else:
            if not size:
                size = (1, 1)
            texture = pygame.Surface(size)
            texture.fill(self.color)
            self.texture = Texture(texture)
        # parent.add_child(self)

        # self.position = (0, 0)
        self.rect = self.texture.image.get_rect()
        self.rect.topleft = (0, 0)
        self.anchor_point = (0.5, 0.5)
        # self.parent = parent
        # self.children = []
        self.rotation = 0.0  # rads
        self.blend_mode = blend_mode

    def _update_children(self, view):
        for kid in self.children:
            kid._update_children(view)
        pos = self.rect
        pos.x = -pos.w * self.anchor_point[0]
        pos.x += self.position[0]
        pos.y = -pos.h * self.anchor_point[1]
        pos.y += self.position[1]
        view.screen.blit(self.texture.image, pos)

    @property
    def frame(self):
        r = self.texture.image.get_bounding_rect()
        r.x += self.position[0]
        r.y += self.position[1]
        return Rect(r.x, r.y, r.w, r.h)


pygame.font.init()


class LabelNode(SpriteNode):
    def __init__(self, text, font=('Helvetica', 20), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        self.font = font
        self._pyfont = pygame.font.Font(None, 20)

        self._render()

    def _render(self):
        self.texture = Texture(self._pyfont.render(self.text, True, self.color))


class Scene(EffectNode):
    def __init__(self, _size=None):
        super().__init__()
        if _size:
            self.size = Point(*_size)
        else:
            self.size = None

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
