from panda3d.core import *



appName = "Flying Game"

loadPrcFileData("",
                        """"
                            window-title {}
                            textures-power-2 none
                            """.format(appName))




from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
import sys
sys.path.append(r"C:\Users\avise\Desktop\Games\RenderPipeline-master")
from rpcore import RenderPipeline, SpotLight
rp = RenderPipeline()

class GameBase(ShowBase):
    def __init__(self, autoSetup = True, debug = False):
        rp.set_loading_screen_image("screenshot7.png")
        rp.create(self)
        rp.daytime_mgr.time = 0.43
        
        if autoSetup:
            self.setupLighting()
            self.setupCollision()
        
        if debug:
            base.setFrameRateMeter(True)
            self.accept("1", base.oobe)
            self.accept("s", base.win.saveScreenshot, ["Saved screenshot.png"])

    def setupCollision(self):
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        base.pusher.addInPattern("%fn-into-%in")

    def setupLighting(self):
        pass

    def setMusic(self, path, loops = True, volume = 1):
        sound = loader.loadSfx(path)
        sound.setVolume(volume)
        sound.setLoop(loops)
        sound.play()



class MenuBase:
    def __init__(self):
        self.frame = DirectFrame(
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dBottom, base.a2dTop),
            frameColor = (0, 0, 0, 0),
            image = "models/tex/ground2.png",
            image_scale = (2, 0, 1),
            )
        self.frame.setTransparency(1)

       
        self.hide()

    def makeButton(self, text = "New Button", pos = (0, -0.7), event = "unknown-button", scale = 0.03, hasPadding = True):
        btn = DirectButton(
            text = text,
            frameColor = (
                (0.2,0.2,0.8,1),
                (0.15, 0.15, 0.6, 1)
                ),
            text_scale = scale,
            text_pos = (0, 0),
            scale = 3,
            pos = (pos[0], 0, pos[1]),
            text_fg = (1, 1, 1,1),
            command = base.messenger.send,
            extraArgs = [event],
            rolloverSound = None,
            clickSound = None,
            relief = DGG.FLAT,
            borderWidth = (0.005, 0.005),
            )
        if hasPadding:
            btn["pad"] = (0.1, 0.001)
        return btn
    

    def makeTitle(self, text = "", pos = (0, 0.6), scale = 0.15):
         return DirectLabel(
            scale = scale,
            text_shadow = (0.2, 1, 0.2, 1),
            pos = (pos[0], 0, pos[1]),
            text = text,
            text_fg = (1, 0.2, 0.2, 1),
            frameColor = (0, 0, 0, 0),
            )

    def show(self):
        self.frame.show()

    def hide(self):
        self.frame.hide()

class Menu(MenuBase):
    def __init__(self):
        MenuBase.__init__(self)

        self.title = self.makeTitle("Flying Game", pos = (0, 0.2), scale = 0.18)
        self.title.reparentTo(self.frame)

        self.start = self.makeButton(text = "Play", pos = (0, 0.0), event = "menu-start")
        self.start.reparentTo(self.frame)

        self.quit = self.makeButton(text = "Quit", pos = (0, -0.15), event = "menu-quit")
        self.quit.reparentTo(self.frame)
        
