"""
 * Copyright (C) The Project "Nugget" Team - All Rights Reserved
 * Written by Jordan Maxwell <jordanmax@nxt-studios.com>, May 2nd, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
 """

from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from nugget.audio.AudioManagerBase import AudioManagerBase

__all__ = ['MusicData', 'MusicManager']

class MusicData(object):

    __slots__ = ['path', 'priority', 'looping', 'volume']

    def __init__(self, path, priority=0, looping=True, volume=0.8):
        self.path = path
        self.priority = priority
        self.looping = looping
        self.volume = volume

class MusicManager(AudioManagerBase):

    notify = DirectNotifyGlobal.directNotify.newCategory('MusicManager')

    def __init__(self):
        AudioManagerBase.__init__(self)
        self.__current = None
        self.__playList = []
        self.accept('PandaRestarted', self.requestCurrentMusicFadeIn)

    def delete(self):
        AudioManagerBase.delete()
        self.ignore('PandaRestarted')
        self.__current = None
        self.__playList = []

    def load(self, audioPath, looping=True):
        resp = AudioManagerBase.load(self, audioPath, audioPath, music=True, looping=looping)
        if not self.exists(audioPath):
            self.notify.warning('Failed to load music: %s!' % audioPath)
            return False
        return resp

    def unload(self, audioPath):
        resp = AudioManagerBase.unload(self, audioPath)
        if self.__current and self.__current.path == audioPath:
            self.__current = None
        for song in self.__playList:
            if song.path == audioPath:
                self.__playList.remove(song)
        return resp

    def request(self, audioPath, priority=0, looping=True, volume=0.8):
        if not self.exists(audioPath):
            if not self.load(audioPath, looping):
                return

        found = False
        for song in self.__playList:
            if song.path == audioPath:
                song.priority = priority
                found = True

        if not found:
            song = MusicData(audioPath, priority, looping, volume)
            self.__playList.append(song)
        self.__update()

    def requestCurrentMusicFadeIn(self, duration=3.0, finalVolume=1):
        if self.__current:
            self.requestFadeIn(self.__current, duration, finalVolume)

    def __update(self):
        if len(self.__playList) == 0:
            return

        def comparePriority(a, b):
            if a.priority < b.priority:
                return 1
            elif a.priority > b.priority:
                return -1
            return 0

        self.__playList.sort(comparePriority)

        if self.__current == self.__playList[0]:
            return

        if self.__current:
            current = self.getSource(self.__current.audioPath)
            if current and current.getFinalVolume() > 0:
                self.requestFadeOut(self.__current.path, removeFromPlaylist=True)

        self.__current = self.__playList[0]
        songLength = 207 #TEMP
        if not self.__current.looping:
            if songLength:
                taskMgr.doMethodLater(songLength, self.__currentTrackComplete, 'currentTrackComplete', extraArgs=[self.__current.path])

        self.requestFadeIn(self.__current.path, finalVolume = self.__current.volume)

    def requestFadeOut(self, name, duration=3, finalVolume=0, priority=0, removeFromPlaylist=True):
        self.requestChangeVolume(name, duration, finalVolume, priority, removeFromPlaylist)


    def requestChangeVolume(self, name, duration, finalVolume, priority=0, removeFromPlayList=False):
        AudioManagerBase.requestChangeVolume(self, name, duration, finalVolume, priority)
        if finalVolume == 0:
            requireUpdate = False

            if removeFromPlaylist:
                for song in self.__playList:
                    if song.path == name:
                        self.__playList.remove(song)
                        requireUpdate = True
                        break

            if requireUpdate:
                self.__update()

    def __currentTrackComplete(self, task=None, name=None):
        if name:
            self.requestFadeOut(name, duration=0, removeFromPlaylist=True)
        else:
            pass
        return Task.done


