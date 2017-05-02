"""
 * Copyright (C) The Project "Nugget" Team - All Rights Reserved
 * Written by Jordan Maxwell <jordanmax@nxt-studios.com>, May 2nd, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
 """

from direct.showbase.DirectObject import DirectObject
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

        #Test code
        #self.bgmMusic = base.audioManager.load('menu-music', AudioGlobals.HELLO, True, True)
        #self.bgmMusic.play()
        #base.audioManager.requestFadeIn('menu-music')

        yAxis = -0.8
        self.newGameButton = DirectButton(
            parent=base.a2dTopCenter,
            text='New Game',  
            image_scale=1, 
            scale=0.1, 
            pos=(0, 0, yAxis), 
            command=self.__handleNewGame)   
        yAxis -= 0.15 
        self.resumeGameButton = DirectButton(
            parent=base.a2dTopCenter,
            text='Resume Game',  
            image_scale=1, 
            scale=0.1, 
            pos=(0, 0, yAxis), 
            command=self.__handleResumeGame)   
        yAxis -= 0.15   
        self.settingsButton = DirectButton(
            parent=base.a2dTopCenter,
            text='Settings',  
            image_scale=1, 
            scale=0.1, 
            pos=(0, 0, yAxis), 
            command=self.__handleSettings)   
        yAxis -= 0.15   
        self.quitButton = DirectButton(
            parent=base.a2dTopCenter,
            text='Quit',  
            image_scale=1, 
            scale=0.1, 
            pos=(0, 0, yAxis), 
            command=self.__handleQuit)

    def unload(self):
        if not self.__isLoaded:
            return

        self.newGameButton.destroy()
        del self.newGameButton
        self.resumeGameButton.destroy()
        del self.resumeGameButton
        self.settingsButton.destroy()
        del self.settingsButton
        self.quitButton.destroy()
        del self.quitButton

    def __handleNewGame(self):
        pass

    def __handleResumeGame(self):
        pass

    def __handleSettings(self):
        pass

    def __handleQuit(self):
        messenger.send(self.doneEvent, [{'mode': 'exit'}])