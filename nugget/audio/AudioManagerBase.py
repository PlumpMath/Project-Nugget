"""
 * Copyright (C) The Project "Nugget" Team - All Rights Reserved
 * Written by Jordan Maxwell <jordanmax@nxt-studios.com>, May 2nd, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
 """

from direct.showbase.DirectObject import DirectObject
from direct.directnotify import DirectNotifyGlobal
from nugget.audio.AudioSource import AudioSource

class AudioManagerBase(DirectObject):

    notify = DirectNotifyGlobal.directNotify.newCategory('AudioManagerBase')
    __slots__ = ['__audioSources', '__masterVolume']

    def __init__(self):
        self.__audioSources = {}
        self.__masterVolume = 1.0

    def load(self, name, audioPath, looping=True, music=False):
        if self.exists(name):
            self.notify.warning('Unable to load %s; Audio source key already eixsts.' % name)
            return True
        source = AudioSource(audioPath, looping, music)
        self.__audioSources[name] = source
        return False

    def unload(self, name):
        if not self.exists(name):
            self.notify.warning('Unable to unload %s; Audio source does not exist' % name)
            return False
        self.__audioSources[name].unload()
        del self.__audioSources[name]
        return True

    def exists(self, name):
        return name in self.__audioSources

    def delete(self):
        for name in self.__audioSources.keys():
            self.__audioSources[name].unload()
        self.__audioSources = {}

    def silence(self):
        for name in self.__audioSources.keys():
            self.__audioSources[name].requestChangeVolume(0, 0, priority=1)

    def requestChangeVolume(self, name, duration, finalVolume, priority=0):
        if not self.exists(name):
            self.notify.warning('Unable to change volume of %s; Audio source does not exist' % name)
            return
        self.__audioSources[name].requestChangeVolume(duration, finalVolume, priority)

    def requestFadeIn(self, name, duration=5, finalVolume=1, priority=0):
        self.requestChangeVolume(name, duration, finalVolume, priority)

    def requestFadeOut(self, name, duration=5, finalVolume=0, priority=0):
        self.requestChangeVolume(name, duration, finalVolume, priority)

    def getSource(self, name):
        if not self.exists(name):
            return None
        return self.__audioSources[name]



