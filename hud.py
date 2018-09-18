from direct.gui.DirectGui import *
from direct.gui.OnscreenText import *
import time

class Hud:
    def __init__(self):
        self.frame = DirectFrame(
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dBottom, base.a2dTop),
            frameColor = (0, 0, 0, 0),
            image_scale = (2, 0, 1),
            enableEdit = False,
            )
        self.frame.setTransparency(0)

        self.title = DirectLabel(
            scale = 0.05,
            pos = (0, 0, 0.9),
            text = "Current Mission Placeholder",
            text_fg = (0.2, 0.2, 0.1, 1),
            frameColor = (0.1, 0.8, 0.8, 0),
            enableEdit = False,
            )

        self.createBtn("Quit", 0.8, ["game-quit"])
        self.createBtn("Found It", 0.7, ["game-finished"])
        self.title.reparentTo(self.frame)

        self.timer = OnscreenText(text = "", mayChange = True, pos = (0.8, 0.9))

        self.hide()

    def createBtn(self, text, verticalPos, commands):
        btn = DirectButton(
            text = text,
            text_fg = (0.2,0.2,0.4,1),
            text_scale = 0.03,
            text_pos = (0, 0),
            scale = 3,
            pos = (-0.9, 0, verticalPos),
            relief = 1,
            frameColor = (0,1,0,0.5),
            command = base.messenger.send,
            extraArgs = commands,
            rolloverSound = None,
            clickSound = None)
        btn.reparentTo(self.frame)

    def show(self):
        self.frame.show()

    def hide(self):
        self.frame.hide()

    def hudTask(self, task):
        self.timer.setText(str(self.missionLength - int(time.time() - self.startTime)) + " seconds left")
        return task.cont

    def initialise(self, currentMission, missionLength):
        self.startTime = time.time()
        self.missionLength = missionLength
        self.title["text"] = currentMission
