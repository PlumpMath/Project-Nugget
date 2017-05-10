"""
 * Copyright (C) The Project "Nugget" Team - All Rights Reserved
 * Written by Jordan Maxwell <jordanmax@nxt-studios.com>, May 2nd, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
 """
from panda3d.core import NodePath, TextNode, Filename, DSearchPath, VirtualFileSystem
from direct.interval.IntervalGlobal import LerpFunctionInterval
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.fsm.StateData import StateData
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from nugget.audio import AudioGlobals

class MainMenu(DirectObject, StateData):

    notify = DirectNotifyGlobal.directNotify.newCategory('MainMenu')

    def __init__(self, doneEvent):
        DirectObject.__init__(self)
        StateData.__init__(self, doneEvent)
        self.__isLoaded = False

    def enter(self):
        self.notify.debug('MainMenu.enter')
        if not self.__isLoaded:
            self.load()

    def exit(self):
        if not self.__isLoaded:
            return
        self.unload()

    def load(self):
        if self.__isLoaded:
            return
        self.__isLoaded = True
        #base.musicMgr.load(AudioGlobals.HELLO)
        #base.musicMgr.request(AudioGlobals.HELLO)

        self.backgroundScreen = loader.loadModel('models/gui/titlescreen.egg')
        self.backgroundScreen.reparentTo(base.aspect2d)
        self.backgroundScreen.setPos(0, 2.73, 0)
        self.backgroundScreen.setScale(3, 1, 2)
        self.backgroundScreen.setBin('background', 1)

        self.buttonParent = NodePath('menu-button-parent')
        self.buttonParent.reparentTo(base.a2dTopLeft)
        self.buttonParent.setPos(0.55, 0, 0)

        yAxis = -0.8
        self.newGameButton = DirectButton(
            parent=self.buttonParent,
            text='New Game',  
            image_scale=1, 
            scale=0.1, 
            pos=(0, 0, yAxis), 
            command=self.__handleNewGame)   
        yAxis -= 0.15 
        self.resumeGameButton = DirectButton(
            parent=self.buttonParent,
            text='Resume Game',  
            image_scale=1, 
            scale=0.1, 
            pos=(0, 0, yAxis), 
            command=self.__handleResumeGame)   
        yAxis -= 0.15   
        self.settingsButton = DirectButton(
            parent=self.buttonParent,
            text='Settings',  
            image_scale=1, 
            scale=0.1, 
            pos=(0, 0, yAxis), 
            command=self.__handleSettings)   
        yAxis -= 0.15   
        self.quitButton = DirectButton(
            parent=self.buttonParent,
            text='Quit',  
            image_scale=1, 
            scale=0.1, 
            pos=(0, 0, yAxis), 
            command=self.__handleQuit)

        self.__loadCredits()

    def unload(self):
        if not self.__isLoaded:
            return
        base.musicMgr.unload(AudioGlobals.HELLO)

        self.newGameButton.destroy()
        del self.newGameButton
        self.resumeGameButton.destroy()
        del self.resumeGameButton
        self.settingsButton.destroy()
        del self.settingsButton
        self.quitButton.destroy()
        del self.quitButton
        del self.buttonParent

    def __handleNewGame(self):
        pass

    def __handleResumeGame(self):
        pass

    def __handleSettings(self):
        pass

    def __handleQuit(self):
        messenger.send(self.doneEvent, [{'mode': 'exit'}])


    def __loadCredits(self):
        self.creditsParent = NodePath('credits-parent')
        self.creditsParent.reparentTo(base.a2dTopRight)
        self.creditsParent.setPos(-1.2, 0, -0.75)

        vfs = VirtualFileSystem.getGlobalPtr()
        filename = Filename('credits.txt')
        searchPath = DSearchPath()
        if __debug__:
            searchPath.appendDirectory(Filename.expandFrom('resources/etc'))
        else:
            searchPath.appendDirectory(Filename.expandFrom('etc'))

        found = vfs.resolveFilename(filename, searchPath)
        if not found:
            self.notify.warning('Unable to load credits; credits.txt not found on %s' % searchPath)
            return

        self.creditsData = vfs.readFile(filename, 1).split('\n')
        self.creditsText = []
        self.currentCreditIndex = 0

        cyAxis = 0
        firstPass = True
        for i in range(0, len(self.creditsData)):
            if i % 5 == 0 and i >= 5:
                firstPass = False
                cyAxis = 0
            text = TextNode('credits-node-%s' % i)
            text.setText(self.creditsData[i])
            self.creditsText.append(text)
            if not firstPass:
                text.setTextColor(255, 255, 255, 0)
            textNodePath = self.creditsParent.attachNewNode(text)
            textNodePath.setScale(0.07)
            textNodePath.setPos(0, 0, cyAxis)
            cyAxis -= 0.1

        taskMgr.doMethodLater(5, self.__processCreditsTask, 'process-credits-task')

    def __processCreditsTask(self, task):
        endIndex = self.currentCreditIndex + 5
        for i in range(self.currentCreditIndex, endIndex):
            if i < len(self.creditsText):
                self.creditsText[i].setTextColor(255, 255, 255, 0)

        self.currentCreditIndex += 5
        endIndex = self.currentCreditIndex + 5
        for i in range(self.currentCreditIndex, endIndex):
            if i < len(self.creditsText):
                self.creditsText[i].setTextColor(255, 255, 255, 1)    

        if (self.currentCreditIndex + 5)>= len(self.creditsText):
            self.currentCreditIndex = -5

        return task.again
        



