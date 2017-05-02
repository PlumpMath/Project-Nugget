"""
 * Copyright (C) The Project "Nugget" Team - All Rights Reserved
 * Written by Jordan Maxwell <jordanmax@nxt-studios.com>, May 1st, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
 """

from direct.directnotify import DirectNotifyGlobal
import json

class GameSave(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('GameSave')

    def __init__(self):
        pass

    def createDefaults(self):
        pass

    def load(self):
        pass

    def write(self):
        pass
