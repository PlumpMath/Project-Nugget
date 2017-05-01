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
