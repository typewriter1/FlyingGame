from direct.gui.DirectGui import *
from gamebase import MenuBase

class MissionSelect(MenuBase):
    def __init__(self):
        MenuBase.__init__(self)
        
        self.title = self.makeTitle(text = "Select Mission")
        self.title.reparentTo(self.frame)

        self.m1 = self.makeButton(text = "1", pos = (-0.5, -0.1), event = "missionselect-m1", hasPadding = False)
        self.m2 = self.makeButton(text = "2", pos = (-0.35, -0.1), event = "missionselect-m2", hasPadding = False)
        self.m3 = self.makeButton(text = "test", pos = (-0.2, -0.1), event = "missionselect-test", hasPadding = False)

        for btn in [self.m1, self.m2, self.m3]:
            btn.reparentTo(self.frame)
        

        self.hide()

