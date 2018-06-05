import pygame
from scene.geometry import Point, Rect, Size
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
        self.color = colours("gray")
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
            self.scene.size = Size(*self.size)

        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        self.bounds = get_bounds(pygame.display.get_wm_info()["window"])

        # self.scene.view = self
        self.tee = Tee(self)
        self.tee.size = self.size

        self.scene.color = self.color
        self.scene.setup()
        self._loop()

    def _loop(self):
        while self.running:
            self.tee.loop(pygame.event.get())
            self.screen.fill(self.scene.color)
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
        self._root = None
        self.children = []
        if parent:
            parent.add_child(self)
        # attributes
        # self.bbox
        # self._alpha
        # self.frame

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
        return Point(*self._position)

    @position.setter
    def position(self, position):
        self._position = Point(*position)

    def add_child(self, node):
        node.parent = self
        self.children.append(node)
        self._new_root(self.parent._root)

    def _new_root(self, root):
        for kid in self.children:
            kid._new_root(root)
        self._root = root

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

    def point_to_scene(self, point):  # todo make rotation work
        point = self._position + point
        return point

    def point_from_scene(self, point):  # todo
        point = -self._position + point
        return point

    def run_action(self, action, key=""):  # TODO add actions
        pass


class EffectNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SpriteNode(Node):
    def __init__(self, texture=None, position=(0, 0), z_position=0.0, scale=1.0,
                 x_scale=1.0, y_scale=1.0, alpha=1.0, speed=1.0, parent=None,
                 size=None, color="white", blend_mode=0
                 ):
        super().__init__(position=position, z_position=z_position, scale=scale,
                         x_scale=x_scale, y_scale=y_scale, alpha=alpha, speed=speed, parent=parent)

        self.color = colours(color)
        self._size = 0
        if texture:
            if isinstance(texture, str):
                texture = Texture(texture)
            self.texture = texture
            if size:
                self.size = size
            else:
                size = self.texture.image.get_size()
        else:
            if not size:
                size = (1, 1)
            texture = pygame.Surface(size)

            texture.fill(self.color)
            self.texture = Texture(texture)
            size = self.texture.image.get_size()
        self._size = size
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
        pos.y = pos.h * (1 - self.anchor_point[1])
        pos.y += self.position[1]
        pos.y = self._root.size.y - pos.y
        # view.screen.blit(self.texture.image, pos)
        view.screen.blit(pygame.transform.smoothscale(self.texture.original, (self._size[0], self._size[1])), pos)

    @property
    def frame(self):
        r = self.texture.image.get_bounding_rect()
        r.x += self.position[0]
        r.y += self.position[1]
        return Rect(r.x, r.y, r.w, r.h)

    @property
    def alpha(self):
        return self.texture.image.get_alpha()
        # return self._alpha

    @alpha.setter
    def alpha(self, alpha):
        self.texture.image.set_alpha(alpha)
        self._alpha = alpha

    @property
    def size(self):
        return Size(*self._size)  # todo add gget

    @size.setter
    def size(self, size):  # todo see if there is a better way to do this

        self.texture.image = pygame.transform.scale(self.texture.original, (size[0], size[1]))

        self._size = size


pygame.font.init()

class LabelNode(SpriteNode):
    def __init__(self, text, font=('Helvetica', 20), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        self.font = font
        self._pyfont = pygame.font.Font(None, font[1])

        self._render()

    def _render(self):
        self.texture = Texture(self._pyfont.render(self.text, True, self.color))


class Scene(EffectNode):
    def __init__(self, _size=None, color="gray", *args, **kwargs):
        super().__init__(*args, **kwargs)
        if _size:
            self.size = Size(*_size)
        else:
            self.size = None
        self.color = colours(color)
        self.parent = self
        self._root = self

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

    @property
    def bounds(self):

        return Rect(0, 0, self.size[0], self.size[1])

_colourdic = {'aliceblue': (240, 248, 255),
              'antiquewhite': (250, 235, 215),
              'aqua': (0, 255, 255),
              'aquamarine': (127, 255, 212),
              'azure': (240, 255, 255),
              'beige': (245, 245, 220),
              'bisque': (255, 228, 196),
              'black': (0, 0, 0),
              'blanchedalmond': (255, 235, 205),
              'blue': (0, 0, 255),
              'blueviolet': (138, 43, 226),
              'brown': (165, 42, 42),
              'burlywood': (222, 184, 135),
              'cadetblue': (95, 158, 160),
              'chartreuse': (127, 255, 0),
              'chocolate': (210, 105, 30),
              'coral': (255, 127, 80),
              'cornflowerblue': (100, 149, 237),
              'cornsilk': (255, 248, 220),
              'crimson': (220, 20, 60),
              'cyan': (0, 255, 255),
              'darkblue': (0, 0, 139),
              'darkcyan': (0, 139, 139),
              'darkgoldenrod': (184, 134, 11),
              'darkgray': (169, 169, 169),
              'darkgrey': (169, 169, 169),
              'darkgreen': (0, 100, 0),
              'darkkhaki': (189, 183, 107),
              'darkmagenta': (139, 0, 139),
              'darkolivegreen': (85, 107, 47),
              'darkorange': (255, 140, 0),
              'darkorchid': (153, 50, 204),
              'darkred': (139, 0, 0),
              'darksalmon': (233, 150, 122),
              'darkseagreen': (143, 188, 143),
              'darkslateblue': (72, 61, 139),
              'darkslategray': (47, 79, 79),
              'darkslategrey': (47, 79, 79),
              'darkturquoise': (0, 206, 209),
              'darkviolet': (148, 0, 211),
              'deeppink': (255, 20, 147),
              'deepskyblue': (0, 191, 255),
              'dimgray': (105, 105, 105),
              'dimgrey': (105, 105, 105),
              'dodgerblue': (30, 144, 255),
              'firebrick': (178, 34, 34),
              'floralwhite': (255, 250, 240),
              'forestgreen': (34, 139, 34),
              'fuchsia': (255, 0, 255),
              'gainsboro': (220, 220, 220),
              'ghostwhite': (248, 248, 255),
              'gold': (255, 215, 0),
              'goldenrod': (218, 165, 32),
              'gray': (128, 128, 128),
              'grey': (128, 128, 128),
              'green': (0, 128, 0),
              'greenyellow': (173, 255, 47),
              'honeydew': (240, 255, 240),
              'hotpink': (255, 105, 180),
              'indianred': (205, 92, 92),
              'indigo': (75, 0, 130),
              'ivory': (255, 255, 240),
              'khaki': (240, 230, 140),
              'lavender': (230, 230, 250),
              'lavenderblush': (255, 240, 245),
              'lawngreen': (124, 252, 0),
              'lemonchiffon': (255, 250, 205),
              'lightblue': (173, 216, 230),
              'lightcoral': (240, 128, 128),
              'lightcyan': (224, 255, 255),
              'lightgoldenrodyellow': (250, 250, 210),
              'lightgray': (211, 211, 211),
              'lightgrey': (211, 211, 211),
              'lightgreen': (144, 238, 144),
              'lightpink': (255, 182, 193),
              'lightsalmon': (255, 160, 122),
              'lightseagreen': (32, 178, 170),
              'lightskyblue': (135, 206, 250),
              'lightslategray': (119, 136, 153),
              'lightslategrey': (119, 136, 153),
              'lightsteelblue': (176, 196, 222),
              'lightyellow': (255, 255, 224),
              'lime': (0, 255, 0),
              'limegreen': (50, 205, 50),
              'linen': (250, 240, 230),
              'magenta': (255, 0, 255),
              'maroon': (128, 0, 0),
              'mediumaquamarine': (102, 205, 170),
              'mediumblue': (0, 0, 205),
              'mediumorchid': (186, 85, 211),
              'mediumpurple': (147, 112, 219),
              'mediumseagreen': (60, 179, 113),
              'mediumslateblue': (123, 104, 238),
              'mediumspringgreen': (0, 250, 154),
              'mediumturquoise': (72, 209, 204),
              'mediumvioletred': (199, 21, 133),
              'midnightblue': (25, 25, 112),
              'mintcream': (245, 255, 250),
              'mistyrose': (255, 228, 225),
              'moccasin': (255, 228, 181),
              'navajowhite': (255, 222, 173),
              'navy': (0, 0, 128),
              'oldlace': (253, 245, 230),
              'olive': (128, 128, 0),
              'olivedrab': (107, 142, 35),
              'orange': (255, 165, 0),
              'orangered': (255, 69, 0),
              'orchid': (218, 112, 214),
              'palegoldenrod': (238, 232, 170),
              'palegreen': (152, 251, 152),
              'paleturquoise': (175, 238, 238),
              'palevioletred': (219, 112, 147),
              'papayawhip': (255, 239, 213),
              'peachpuff': (255, 218, 185),
              'peru': (205, 133, 63),
              'pink': (255, 192, 203),
              'plum': (221, 160, 221),
              'powderblue': (176, 224, 230),
              'purple': (128, 0, 128),
              'red': (255, 0, 0),
              'rosybrown': (188, 143, 143),
              'royalblue': (65, 105, 225),
              'saddlebrown': (139, 69, 19),
              'salmon': (250, 128, 114),
              'sandybrown': (244, 164, 96),
              'seagreen': (46, 139, 87),
              'seashell': (255, 245, 238),
              'sienna': (160, 82, 45),
              'silver': (192, 192, 192),
              'skyblue': (135, 206, 235),
              'slateblue': (106, 90, 205),
              'slategray': (112, 128, 144),
              'slategrey': (112, 128, 144),
              'snow': (255, 250, 250),
              'springgreen': (0, 255, 127),
              'steelblue': (70, 130, 180),
              'tan': (210, 180, 140),
              'teal': (0, 128, 128),
              'thistle': (216, 191, 216),
              'tomato': (255, 99, 71),
              'turquoise': (64, 224, 208),
              'violet': (238, 130, 238),
              'wheat': (245, 222, 179),
              'white': (255, 255, 255),
              'whitesmoke': (245, 245, 245),
              'yellow': (255, 255, 0),
              'yellowgreen': (154, 205, 50)}


def colours(c):  # todo return 4 vaules
    """turns an imput in to a typle.
    eg ffffff > (255, 255, 255) or 'black' > (0, 0, 0)"""
    if isinstance(c, str):
        if c in _colourdic:
            return _colourdic[c]
        elif c[0] == "#" and len(c) == 7:
            return tuple(int(c[1:][i:i + 2], 16) for i in (0, 2, 4))
        else:
            raise "not a valid colour"
    else:
        try:
            return (int(c[0]), int(c[1]), int(c[2]))
        except Exception:
            raise "not a valid colour"
