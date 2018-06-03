from scene.other import Touch

RCLICK     = -1
MCLICK     = -2
LCLICK     = -3
SCROLLUP   = -4
SCROLLDOWN = -5

QUIT            = 12
MOUSEBUTTONDOWN = 5
MOUSEBUTTONUP   = 6
MOUSEMOTION     = 4
KEYDOWN         = 2
KEYUP           = 3

class Tee:
    def __init__(self, view):
        self.downcall = view.scene.touch_began
        self.movecall = view.scene.touch_moved
        self.endcall = view.scene.touch_ended
        self.quitcall = view._quit
        self.owner = view

    def loop(self, events):
        for event in events:
            if event.type == QUIT:
                self.quitcall()
            elif event.type == MOUSEBUTTONDOWN:
                self.downcall(Touch(event.pos[0], event.pos[1], event.pos[0], event.pos[1], -event.button))
            elif event.type == MOUSEMOTION:
                for i in range(len(event.buttons)):
                    if event.buttons[i]:
                        self.movecall(Touch(event.pos[0], event.pos[1], event.rel[0], event.rel[1], -i-1))
            elif event.type == MOUSEBUTTONUP:
                self.endcall(Touch(event.pos[0], event.pos[1], event.pos[0], event.pos[1], -event.button))
            elif event.type == KEYDOWN:
                print(event.key)
                self.downcall(Touch(-1, -1, -1, -1, event.key))
            elif event.type == KEYUP:
                self.endcall(Touch(-1, -1, -1, -1, event.key))

    def get_list(self):  # todo add list for points and link it to the scene
        return
