"""
 * Copyright (C) The Project "Nugget" Team - All Rights Reserved
 * Written by Jordan Maxwell <jordanmax@nxt-studios.com>, May 2nd, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
 """

from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import LerpFunc, Sequence

class AudioSource(object):

    notify = DirectNotifyGlobal.directNotify.newCategory('AudioSource')
    __slots__ = [
        '__audioPath', '__loop', '__music', '__currentPriority', '__duration',
        '__startVolume', '__finalVolume', '__currentActionInterval', 
        '__masterVolume', '__sfx']

    def __init__(self, audioPath, masterVolume, loop=True, music=False):
        self.__audioPath = audioPath
        self.__loop = loop
        self.__music = music
        self.__currentPriority = 0
        self.__duration = 0
        self.__startVolume = 0
        self.__finalVolume = 0
        self.__currentActionInterval = None
        self.__masterVolume = masterVolume
        if self.__music:
            self.__sfx = loader.loadMusic(audioPath)
        else:
            self.__sfx = loader.loadSfx(audioPath)
        self.setLoop(self.__loop)
        self.setVolume(0)

    def getSfx(self):
        return self.__sfx

    def getAudioPath(self):
        return self.__audioPath

    def setVolume(self, volume):
        self.__sfx.setVolume(volume)

    def getVolume(self):
        return self.__sfx.getVolume()

    def setLoop(self, loop):
        self.__sfx.setLoop(loop)

    def getLoop(self):
        return self.__sfx.getLoop()

    def getStartVolume(self):
        return self.__startVolume

    def getFinalVolume(self):
        return self.__finalVolume

    def play(self):
        self.__sfx.play()

    def stop(self):
        self.__sfx.stop()

    def unload(self):
        self.stop()

    def changeMasterVolume(self, masterVolume):
        if self.__masterVolume != masterVolume:
            self.__masterVolume = masterVolume
            if self.__currentActionInterval and self.__currentActionInterval.isPlaying():
                pass
            elif self.sfx.status() == 2:
                vol = float(self.__finalVolume) * self.__masterVolume
                self.__sfx.setVolume(vol)

    def requestChangeVolume(self, duration, finalVolume, priority):
        if priority < self.__currentPriority:
            return
        self.__currentPriority = priority
        self.__duration = duration
        self.__startVolume = self.getVolume()
        self.__finalVolume = finalVolume
        if self.__currentActionInterval:
            self.__currentActionInterval.pause()
            self.__currentActionInterval = None
        self.__currentActionInterval = Sequence(
            LerpFunc(
                self.__changeVolumeTask,
                fromData=self.__startVolume,
                toData=self.__finalVolume,
                duration=self.__duration))
        self.__currentActionInterval.start()

    def __changeVolumeTask(self, val):
        curVolume = val * self.__masterVolume
        self.setVolume(curVolume)
        if curVolume > 0 and self.__sfx.status() == 1:
            self.play()
        elif curVolume <= 0 and self.__sfx.status() == 2:
            self.stop()
            self.__currentPriority = 0


