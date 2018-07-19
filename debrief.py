from direct.gui.DirectGui import *
from gamebase import MenuBase

class Debrief(MenuBase):
    def __init__(self):
        MenuBase.__init__(self)

        self.title = self.makeTitle(text = "Placeholder for question")
        self.title.reparentTo(self.frame)

        self.btn1 = self.makeButton(text = "3", pos = (-0.2, -0.6), event = "debrief-correct", hasPadding = False)
        self.btn2 = self.makeButton(text = "5", pos = (0, -0.6), event = "debrief-wrong", hasPadding = False)
        self.btn3 = self.makeButton(text = "2", pos = (0.2, -0.6), event = "debrief-wrong", hasPadding = False)

        for btn in [self.btn1, self.btn2, self.btn3]:
             btn.reparentTo(self.frame)
            
        self.backBtn = self.makeButton(text = "Back", pos = (-0.9, -0.8), event = "debrief-back")
        self.backBtn.reparentTo(self.frame)

        self.restartBtn = self.makeButton(text = "Restart", pos = (-0.9, -0.6), event = "debrief-restart")
        self.restartBtn.reparentTo(self.frame)

        self.hide()
        self.chosenAnswer = False

    def setTitle(self, newTitle, isAnswer = True):
        """isAnswer should be true if you are setting the title to a chosen answer"""
        if not self.chosenAnswer:
            self.title["text"] = newTitle
        self.backBtn.show()
        if isAnswer:
            self.chosenAnswer = True

    def setButtons(self, values):
        assert type(values) in (list, tuple) and len(values) == 3, "Values must be a list of length 3"
        self.btn1["text"] = values[0]
        self.btn2["text"] = values[1]
        self.btn3["text"] = values[2]

    def initialise(self):
        """Re-initialises the screen"""
        self.chosenAnswer = False
        self.title["text"] = ""

