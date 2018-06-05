# global states
# =====================================

def blend_mode(mode):  # todo add
    pass


def fill(r=0, g=0, b=0, a=1):
    pass


def no_fill():
    pass


def no_fill():
    pass


def no_tint():
    pass


def stroke(r, g, b, a=1):
    pass


def stroke_weight(line_width):
    pass


def use_shader(shader):
    pass


# drawing
# =====================================

def background(r=0, g=0, b=0):
    pass


def ellipse(x=0, y=0, w=0, h=0):
    pass


def image(name, x=0, y=0, w=0, h=0[, from_x, from_y, from_w, from_h]

):
pass


def image_quad(name, x1, y1, x2, y2, x3, y3, x4, y4[, from_x1, from_y1, from_x2, from_y2, from_x3, from_y3, from_x4,
                                                      from_y4]

):
pass


def line(x1, y1, x2, y2):
    pass


def rect(x=0, y=0, w=0, h=0):
    pass


def text(txt, font_name='Helvetica', font_size=16.0, x=0.0, y=0.0, alignment=5):
    pass


def tint(r=1, g=1, b=1, a=1):
    pass


def triangle_strip(points[, tex_coords, image_name]

):
pass


# Coordinate Transformation
# =====================================

def translate(x, y):
    pass


def pop_matrix():
    pass


def push_matrix():
    pass


def rotate(deg):
    pass


def scale(x, y):
    pass


# Loading Images
# =====================================

def load_image(image_name):
    pass


def load_image_file(image_path):
    pass


def load_pil_image(image):
    pass


def render_text(txt, font_name='Helvetica', font_size=16.0):
    pass


def unload_image(image_name):
    pass
