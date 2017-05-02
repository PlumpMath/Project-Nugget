"""
 * Copyright (C) The Project "Nugget" Team - All Rights Reserved
 * Written by Jordan Maxwell <jordanmax@nxt-studios.com>, May 1st, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
 """

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
            string += 'win-size ' + self.getWidth().__repr__() + ' ' + self.getHeight().__repr__() + '\n'
            string += 'fullscreen ' + self.getFullscreen().__repr__() + '\n'    
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

        self.version = self.verify(data, int, 'version', self.OPTIONS_VERSION)
        self.window_width = self.verify(data, int, 'window_width', 800)
        self.window_height = self.verify(data, int, 'window_height', 600)
        self.fullscreen_width = self.verify(data, int, 'fullscreen_width', 800)
        self.fullscreen_height = self.verify(data, int, 'fullscreen_height', 600)
        self.fullscreen = self.verify(data, bool, 'fullscreen', False)
        self.sound = self.verify(data, bool, 'sound', True)
        self.sound_volume = self.verify(data, float, 'sound_volume', 1.0)
        self.music = self.verify(data, bool, 'music', True)
        self.music_volume = self.verify(data, float, 'music_volume', 1.0)
        self.frame_rate = self.verify(data, bool, 'frame_rate', False)

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
        settingsFile.write(json.dumps(data, sort_keys=True, indent=4))
        settingsFile.close()

    def verify(self, data, type, value, default):
        if value not in data:
            return default
        value = data[value]
        if not isinstance(value, type):
            self.notify.warning('%s is not a instance of %s! Setting default value.' % (value, type.__name__))
            return default
        return value

    def __str__(self):
        output = 'Version: %s\n' % self.version
        output += 'Window Width: %s\n' % self.window_width
        output += 'Window Height: %s\n' % self.window_height
        output += 'Fullscreen Width: %s\n' % self.fullscreen_width
        output += 'Fullscreen Height: %s\n' % self.fullscreen_height
        output += 'Fullscreen: %s\n' % self.fullscreen
        output += 'Sound: %s\n' % self.sound
        output += 'Sound Volume: %s\n' % self.sound_volume
        output += 'Music: %s\n' % self.music
        output += 'Music Volume: %s\n' % self.music_volume
        output += 'Frame Rate: %s\n' % self.frame_rate
        return output

