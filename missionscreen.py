from direct.gui.DirectGui import *
from panda3d.core import *
from gamebase import MenuBase

class MissionScreen(MenuBase):
    def __init__(self):
        MenuBase.__init__(self)
       
        self.title = self.makeTitle(text = "Mission Placeholder")
        self.title.reparentTo(self.frame)

        self.startBtn = self.makeButton(text = "Start", pos = (0, -0.7), event = "mission-start")
        self.startBtn.reparentTo(self.frame)

        self.hide()

    def showWithTitle(self, titleText):
        self.show()
        self.title["text"] = titleText

