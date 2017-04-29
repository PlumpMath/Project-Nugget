from panda3d.core import Filename, ExecutionEnvironment, WindowProperties
from nugget.nuggetbase.GameStateFSM import GameStateFSM
from direct.showbase.ShowBase import ShowBase
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.task import Task
import __builtin__
import time
import os

class NuggetBase(ShowBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('NuggetBase')

    def __init__(self):
        ShowBase.__init__(self)
        __builtin__.__dev__ = config.GetBool('want-dev', False)

        self.__fpsEnabled = False
        self.__isMainWindowOpen = False

        if __dev__:
            self.notify.info('Starting in Development mode.')
            self.accept('f1', self.toggleFPS)

        if config.GetBool('want-screenshots', True):
            self.accept('f12', self.takeScreenshot)

        self.gameStateFSM = GameStateFSM()

    def isClientBuilt(self):
        try:
            import buildData
            return True
        except:
            return False

    def toggleFPS(self):
        self.__fpsEnabled = not self.__fpsEnabled
        base.setFrameRateMeter(self.__fpsEnabled)

    def openMainWindow(self, *args, **kw):
        success = ShowBase.openMainWindow(self, *args, **kw)
        if not success:
            self.notify.error('Failed to open game window!')
            return

        if self.win:
            self.win.setSort(500)
            self.win.setChildSort(10)
            self.__postOpenWindow()

        self.__isMainWindowOpen = success
        self.__setCursorAndIcon()

    def __postOpenWindow(self):
        pass

    def __setCursorAndIcon(self):
        wp = WindowProperties()        
        if self.isClientBuilt():
            if sys.platform == 'darwin':
                wp.setIconFilename(Filename.fromOsSpecific(os.path.join(os.getcwd(), 'icon500.ico')))
            else:
                wp.setIconFilename(Filename.fromOsSpecific(os.path.join(os.getcwd(), 'icon256.ico')))
        else:
            wp.setIconFilename(Filename.fromOsSpecific(os.path.join(os.getcwd(), 'resources/etc/icon.ico')))

        if self.config.GetBool('want-custom-cursor', False):
            wp.setCursorFilename(Filename.fromOsSpecific(os.path.join(tempdir, 'pointer.cur')))

        self.win.requestProperties(wp)

    def takeScreenshot(self):
        if not config.GetBool('want-screenshots', True):
            return

        self.notify.info('Taking Screenshot.')
        if not os.path.exists('screenshots'):
            os.mkdir('screenshots')

        dt = time.localtime()
        date_time = '%04d-%02d-%02d_%02d-%02d-%02d' % (dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])
        uFilename = 'screenshots/screenshot_' + date_time + '.' + base.screenshotExtension
        pandafile = Filename(str(ExecutionEnvironment.getCwd()) + '/' + str(uFilename))
        pandafile.makeDir()
        fn = base.screenshot(namePrefix = uFilename, defaultFilename = 0)
        winfile = pandafile.toOsSpecific()
        self.notify.info('Screenshot captured: ' + winfile)
        screenShotNotice = DirectLabel(text = 'Screenshot Captured:\n' + winfile, scale = 0.050000, pos = (0.0, 0.0, 0.299), text_bg = (1, 1, 1, 0), text_fg = (1, 1, 1, 1), frameColor = (1, 1, 1, 0))
        screenShotNotice.reparentTo(base.a2dBottomCenter)
        screenShotNotice.setBin('gui-popup', 0)

        def clearScreenshotMsg(event):
            screenShotNotice.destroy()

        taskMgr.doMethodLater(3.0, clearScreenshotMsg, 'clearScreenshot')