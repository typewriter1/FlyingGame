from panda3d.core import *
from direct.showbase.ShowBase import *
from direct.fsm.FSM import FSM
from direct.gui.OnscreenText import OnscreenText
from direct.particles.ParticleEffect import ParticleEffect
from gamebase import *
from missionscreen import MissionScreen
from debrief import Debrief
from hud import Hud
from missionselect import MissionSelect
from parsemission import parseMissionFile
from settings import Settings

import sys
import time


class Mission:
    def __init__(self, timeAllowed = 60,
                 objective = "Placeholder objective",
                 question = "Placeholder question",
                 mapName = "models/terrain.egg",
                 options = ["o1", "o2", "o3"],
                 correctAnswer = "o2"):
        self.timeAllowed = timeAllowed
        self.objective = objective
        self.objective += "\n You have " + str(timeAllowed) + " seconds\n to complete the mission."
        self.question = question
        self.mapName = mapName
        self.options = options
        self.correctAnswer = correctAnswer


missions = {
    "m1": Mission(
        timeAllowed = 60,
        objective = "Our Enemy has just been bombed!\n Report how many fuel canisters\n are at their base.",
        question = "So, how many canisters were there?",
        mapName = "models/m1.mission",
        options = ["3", "4", "8"],
        correctAnswer = "3"
        ),
    "m2": Mission(
        timeAllowed = 180,
        objective = "Find both bases\n and report how many helicopters\n they have.",
        question = "So, how many helicopters do they have,in total?",
        mapName = "models/m2.mission",
        options = ["3", "5", "7"],
        correctAnswer = "3"
        ),
    "m3": Mission(
        timeAllowed = 180,
        objective = "The enemy are developing a\n secret new weapon! Find it, and report how many guns it has",
        question = "So, how many wings does it have?",
        mapName = "models/terrain_m1",
        options = ["3", "4", "2"],
        correctAnswer = "3"),
    "test": Mission(
        timeAllowed = 2,
        objective = "This is a test mission",
        question = "Test",
        mapName = "models/m1.mission",
        options = ["t", "t1", "t2"],
        correctAnswer = "t"
        ),
    }

class Game(GameBase, FSM):
    def __init__(self):
        GameBase.__init__(self, debug = True)
        FSM.__init__(self, "GUI FSM")
        base.disableMouse()
        
        self.menu = Menu()
        self.settings = Settings()
        self.missionScreen = MissionScreen()
        self.debrief = Debrief()
        self.hud = Hud()
        self.missionSelect = MissionSelect()

        base.camLens.setFov(90)

        self.setMusic("audio/music.mp3", volume = 0.5)
        self.setMusic("audio/engine1.wav", volume = 0.3)

        self.request("Menu")
        base.taskMgr.add(self.missionOverTask, "is mission over")


    def enterMenu(self):
        self.menu.show()
        self.accept("menu-start", self.request, ["MissionSelect"])
        self.accept("menu-instructions", self.request, ["Instructions"])
        self.accept("menu-quit", sys.exit)
        self.accept("menu-settings", self.request, ["Settings"])

    def exitMenu(self):
        self.menu.hide()
        self.ignore("menu-start")
        self.ignore("menu-instructions")
        self.ignore("menu-quit")

    def enterSettings(self):
        self.settings.show()
        self.accept("settings-back", self.request, ["Menu"])

    def exitSettings(self):
        self.settings.hide()
        self.ignore("settings-back")

    def enterMissionSelect(self):
        self.missionSelect.show()
        self.accept("missionselect-m1", self.setMission, ["m1"])
        self.accept("missionselect-m2", self.setMission, ["m2"])
        self.accept("missionselect-test", self.setMission, ["test"])

    def exitMissionSelect(self):
        self.missionSelect.hide()
        self.ignore("missionselect-m1")
        self.ignore("missionselect-m2")

    def enterMissionScreen(self):
        self.missionScreen.showWithTitle(self.currentMission.objective)
        self.accept("mission-start", self.request, ["Game"])

    def exitMissionScreen(self):
        self.missionScreen.hide()
        self.ignore("mission-start")

    def enterGame(self):
        self.world = World(self.currentMission.mapName)
        self.startTime = "Not yet set - not loaded"  #set in self.missionOverTask
        self.player = Player(self.world)
        self.accept("player-into-Collision", self.player.reset)
        self.accept("game-quit", self.request, ["Menu"])
        self.accept("game-finished", self.request, ["Debrief"])
    
    def exitGame(self):
        self.world.destroy()
        self.player.model.removeNode()
        del self.player
        base.taskMgr.remove("hud update")
        self.hud.timer.setText("")
        self.hud.hide()
        base.taskMgr.remove("update player")
        self.ignore("game-quit")

    def enterDebrief(self):
        self.debrief.show()
        self.debrief.setTitle(self.currentMission.question, isAnswer = False)
        self.debrief.setButtons(self.currentMission)
        self.accept("debrief-correct", self.debrief.setTitle, ["Correct"])
        self.accept("debrief-wrong", self.debrief.setTitle, ["Wrong"])
        self.accept("debrief-back", self.request, ["Menu"])
        self.accept("debrief-restart", self.request, ["Game"])

    def exitDebrief(self):
        self.debrief.hide()
        self.ignore("debrief-correct")
        self.ignore("debrief-wrong")
        self.debrief.initialise() #clear all settings on it, ie title and buttons, as they are mission specific

    def setMission(self, name):
        self.currentMission = missions[name]
        self.request("MissionScreen")

    def missionOverTask(self, task):
        if self.state == "Game" and self.world.loaded and self.startTime == "Not yet set - not loaded":
            self.startTime = time.time()
            self.hud.show()
            self.hud.initialise(self.currentMission.objective, self.currentMission.timeAllowed)
            base.taskMgr.add(self.hud.hudTask, "hud update")
        if self.state == "Game" and self.world.loaded:
            if time.time() - self.startTime > self.currentMission.timeAllowed:
                self.request("Debrief")
        return task.cont


class World:
    def __init__(self, missionMap):
        self.map = missionMap
        base.taskMgr.add(self.loadScene)
        self.loaded = False


    async def loadScene(self, task):
        text = OnscreenText("Loading...")

        self.terrain = await loader.loadModel(models["terrain"], blocking = False)
        self.terrain.reparentTo(render)
        if USE_RENDER_PIPELINE:
            rp.prepare_scene(self.terrain)
        self.terrain.setScale(18)
        

        modelList = parseMissionFile(self.map)
        print(modelList)
        for model in modelList:
            try:
                m = loader.loadModel("models/" + model.modelName)
                m.reparentTo(self.terrain)
                m.setPos(*model.modelPos)
            except:
                #Its a particle system
                floater = render.attachNewNode("particle floater")
                floater.setPos(self.terrain, *model.particlePos)
                floater.setScale(5)
                self.particles = ParticleEffect()
                self.particles.loadConfig(model.ptfFile)
                print(model.particlePos)
                self.particles.start(parent = floater, renderParent = floater)
                #self.particles.setPos(*model.particlePos)
            

        #Once loaded, remove loading text
        text.hide()
        del text

        self.loaded = True

    def show(self):
        self.terrain.show()

    def hide(self):
        self.terrain.hide()

    def destroy(self):
        self.terrain.removeNode()
        del self.terrain
        del self

class Player:
    def __init__(self, worldInstance):
        self.model = loader.loadModel(models["player"])
        self.model.reparentTo(render)
        self.model.setScale(0.3)
        self.model.setZ(19)

        if USE_RENDER_PIPELINE:
            rp.prepare_scene(self.model)
        
        base.taskMgr.add(self.playerUpdate, "update player")

        self.speed = 70

        self.colNode = self.model.attachNewNode(CollisionNode("player"))
        self.colNode.node().addSolid(CollisionSphere(0, 0, 0, 1))
        #self.colNode.show()
        base.cTrav.addCollider(self.colNode, base.pusher)
        base.pusher.addCollider(self.colNode, self.model)

        
        #self.particles = ParticleEffect()
        #self.particles.loadConfig("particles/exhuast.ptf")
        #self.particles.start(parent = self.model, renderParent = render)

        self.worldInstance = worldInstance

    def reset(self, event):
        self.model.setPos(0, 0, 19)
        self.model.setHpr(0, 0, 0)

    def playerUpdate(self, task):
        pressed = base.mouseWatcherNode.isButtonDown

        if self.worldInstance.loaded:

            if pressed(KeyboardButton.right()):
                self.model.setH(self.model, -1.0)
                self.model.setR(self.model, 1.0)
            elif pressed(KeyboardButton.left()):
                self.model.setH(self.model, 1.0)
                self.model.setR(self.model, -1.0)
            if pressed(KeyboardButton.up()):
                self.model.setP(self.model, 2)
                if self.speed > 0:
                    if self.speed < 5:
                        self.speed -= 0.01
            elif pressed(KeyboardButton.down()):
                self.model.setP(self.model, -2)
                if self.speed < 50:
                    self.speed += 0.01

            if self.model.getP() < 0:
                self.model.setP(self.model, 0.5)
            elif self.model.getP() > 0:
                self.model.setP(self.model, -0.5)
            if self.model.getP() > -0.9 and self.model.getP() < 0.9:
                self.model.setP(0)

            if self.model.getR() < 0:
                self.model.setR(self.model, 0.5)
            elif self.model.getR() > 0:
                self.model.setR(self.model, -0.5)
            if self.model.getR() > -0.5 and self.model.getR() < 0.5:
                self.model.setR(0)

            if self.model.getP() == -180:
                self.model.setP(180)
                
            self.model.setY(self.model, self.speed * globalClock.getDt())
            base.camera.setPos(self.model, 0, -9, 2)
            base.camera.lookAt(self.model)
        #print(self.speed)

        return task.cont



g = Game()
g.run()
