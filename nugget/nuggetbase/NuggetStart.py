from panda3d.core import NodePath, Vec4, loadPrcFile
from direct.directnotify.DirectNotifyGlobal import directNotify
import sys
import os

notify = directNotify.newCategory('NuggetStart')

if __debug__:
    loadPrcFile('config/release.prc')
    loadPrcFile('config/dev.prc')

    if os.path.isfile('config/personal.prc'):
        loadPrcFile('config/personal.prc')

notify.info('Starting game.')
import __builtin__

import NuggetBase
NuggetBase.NuggetBase()

if not base.win:
    notify.warning('Unable to open window; aborting.')
    sys.exit()

clearColor = Vec4(0.0, 0.0, 0.0, 1.0)
base.win.setClearColor(clearColor)

def _doExit(*args):
    print ':TaskManager: TaskManager.destroy()'
    os._exit(1)

taskMgr.destroy = _doExit

base.run()