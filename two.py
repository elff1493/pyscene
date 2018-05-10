import pygame



class scene:
    def __init__(self):
        self.t = 0.0
        self.dt = 0.0
        self.fixed_time_step = False
        self.root_layer = None
        self.touches = {}
        self.delayed_invocations = []
        w, h = (200, 200)  # TODO add method for screen size
        self.size = Size(w, h)
        self.bounds = Rect(0, 0, w, h)
        self.presented_scene = None
        self.presenting_scene = None
        self.setup_finished = False