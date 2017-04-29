from direct.fsm.FSM import FSM
from direct.directnotify import DirectNotifyGlobal

class GameStateFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('GameStateFSM')

    def __init__(self):
        FSM.__init__(self, 'GameStateFSM')
        self.request('MainMenu')

    def enterMainMenu(self):
        self.notify.info('Entering Main Menu')

    def exitMainMenu(self):
        pass

    def enterGame(self):
        pass

    def exitGame(self):
        pass