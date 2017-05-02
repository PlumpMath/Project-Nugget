"""
 * Copyright (C) The Project "Nugget" Team - All Rights Reserved
 * Written by Jordan Maxwell <jordanmax@nxt-studios.com>, May 1st, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
 """

from direct.fsm.FSM import FSM
from direct.directnotify import DirectNotifyGlobal
from nugget.mainmenu.MainMenu import MainMenu
import sys

class GameStateFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('GameStateFSM')

    def __init__(self):
        FSM.__init__(self, 'GameStateFSM')
        self.__mainMenu = None
        self.request('MainMenu')

    def enterMainMenu(self):
        self.notify.info('Entering Main Menu')
        self.__mainMenu = MainMenu('menu-done-event')
        self.accept('menu-done-event', self.processMenuDoneEvent)
        self.__mainMenu.enter()

    def exitMainMenu(self):
        if self.__mainMenu:
            self.__mainMenu.exit()
        self.ignore('menu-done-event')

    def enterGame(self):
        pass

    def exitGame(self):
        pass

    def enterShutdown(self):
        self.notify.info('Shutting down....')
        if self.oldState == 'Game':
            pass #TODO
        sys.exit()

    def exitShutdown(self):
        pass

    def processMenuDoneEvent(self, doneStatus):
        if not 'mode' in doneStatus:
            return
        if self.getCurrentStateOrTransition() != 'MainMenu':
            return
        mode = doneStatus['mode']
        if mode == 'exit':
            self.request('Shutdown')