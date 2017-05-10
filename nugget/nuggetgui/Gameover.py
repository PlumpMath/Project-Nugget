"""
 * Copyright (C) The Project "Nugget" Team - All Rights Reserved
 * Written by Jordan Maxwell <jordanmax@nxt-studios.com>, May 2nd, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
 """

from direct.showbase.DirectObject import DirectObject
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.StateData import StateData

class Gameover(DirectObject, StateData):

    notify = DirectNotifyGlobal.directNotify.newCategory('Gameover')

    def __init__(self, doneEvent):
        DirectObject.__init__(self)
        StateData.__init__(self, doneEvent)
        self.__isLoaded = False

    def enter(self):
        self.notify.debug('Gameover.enter')
        if not self.__isLoaded:
            self.load()

    def load(self):
        if self.__isLoaded:
            return
        self.__isLoaded = True

        self.backgroundScreen = loader.loadModel('models/gui/gameover')
        self.backgroundScreen.reparentTo(base.aspect2d)
        self.backgroundScreen.setPos(0, 2.73, 0)
        self.backgroundScreen.setScale(4, 1, 2)
        self.backgroundScreen.setBin('background', 1)

