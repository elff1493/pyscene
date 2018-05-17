from nodes import SceneView

PORTRAIT = 1  # todo add values
LANDSCAPE = 1


def run(scene_to_run, orientation=0, frame_interval=1, anti_alias=False, show_fps=False, multi_touch=True):
    sv = SceneView()
    if orientation == PORTRAIT:
        ui_orientations = ['portrait']
    elif orientation == LANDSCAPE:
        ui_orientations = ['landscape']
    else:
        ui_orientations = None
    sv.anti_alias = anti_alias
    sv.frame_interval = frame_interval
    sv.multi_touch_enabled = multi_touch
    sv.shows_fps = show_fps
    sv.scene = scene_to_run
    sv.present(orientations=ui_orientations)


def gravity():
    return 0, 0, 0


def get_screen_size():
    pass


def get_screen_scale():
    return 1.0


def get_image_path(name):  # TODO implement
    return name


def get_controllers():  # TODO add controller support
    return
