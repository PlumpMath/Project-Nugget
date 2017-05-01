from direct.directnotify import DirectNotifyGlobal
import json
import os

class GameSettings(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('GameSettings')

    OPTIONS_VERSION = 1
    DEFAULT_FILE_PATH = 'settings.json'

    def __init__(self):
        self.__default()

    def __default(self):
        self.version = self.OPTIONS_VERSION
        self.window_width = 800
        self.window_height = 600
        self.fullscreen_width = 800
        self.fullscreen_height = 600
        self.fullscreen = False
        self.sound = True
        self.sound_volume = 1.0
        self.music = True
        self.music_volume = 1.0
        self.frame_rate = False

    def setRuntimeOptions(self):
        base.enableSoundEffects(self.sound)
        base.enableMusic(self.music)
        base.setFrameRateMeter(self.frame_rate)

    def getWidth(self):
        if self.fullscreen:
            return self.fullscreen_width
        else:
            return self.window_width

    def getHeight(self):
        if self.fullscreen:
            return self.fullscreen_height
        else:
            return self.window_height

    def getFullscreen(self):
        return self.fullscreen

    def getWindowed(self):
        return not self.getFullscreen()

    def settingsToPrcData(self):
        string = ''
        if not __debug__:
            string = string + 'win-size ' + self.getWidth().__repr__() + ' ' + self.getHeight().__repr__() + '\n'
            string = string + 'fullscreen ' + self.getFullscreen().__repr__() + '\n'    
        return string        

    def load(self, path):
        
        # Check if a settings file exists. if not save a file and stop there
        if not os.path.exists(path):
            self.notify.debug('Unable to locate %s. Using defaults' % path)
            self.save(path)
            return

        settingsFile = open(path, 'r')
        data = json.loads(settingsFile.read())
        settingsFile.close()

        self.version = int(data['version'])
        self.window_width = int(data['window_width'])
        self.window_height = int(data['window_height'])
        self.fullscreen_width = int(data['fullscreen_width'])
        self.fullscreen_height = int(data['fullscreen_height'])
        self.fullscreen = bool(data['fullscreen'])
        self.sound = bool(data['sound'])
        self.sound_volume = int(data['sound_volume'])
        self.music = bool(data['music'])
        self.music_volume = int(data['music_volume'])
        self.frame_rate = bool(data['frame_rate'])

    def save(self, path):
        
        data = {}
        data['version'] = self.version
        data['window_width'] = self.window_width
        data['window_height'] = self.window_height
        data['fullscreen_width'] = self.fullscreen_width
        data['fullscreen_height'] = self.fullscreen_height
        data['fullscreen'] = self.fullscreen
        data['sound'] = self.sound
        data['sound_volume'] = self.sound_volume
        data['music'] = self.music
        data['music_volume'] = self.music_volume
        data['frame_rate'] = self.frame_rate

        settingsFile = open(path, 'w')
        settingsFile.write(json.dumps(data))
        settingsFile.close()
