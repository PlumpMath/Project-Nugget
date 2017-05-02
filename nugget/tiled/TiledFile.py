"""
 * Copyright (C) The Project "Nugget" Team - All Rights Reserved
 * Written by Jordan Maxwell <jordanmax@nxt-studios.com>, May 1st, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
 """

from panda3d.core import Filename, DSearchPath, VirtualFileSystem
from direct.showbase.DirectObject import DirectObject
from direct.showbase.PythonUtil import Enum
from direct.directnotify import DirectNotifyGlobal
import json
import os

class TileFileException(Exception):
    """
    generic TileFile exception class
    """

class TileFileIOException(IOError):
    """
    TileFile IO related exception class
    """

class TiledFile(DirectObject):

    notify = DirectNotifyGlobal.directNotify.newCategory('TiledFile')
    map_orientations = Enum('orthogonal, isometric, staggered')

    def __init__(self, filePath, fileName):
        self.__filePath = filePath
        self.__fileName = fileName

        vfs = VirtualFileSystem.getGlobalPtr()
        filename = Filename(fileName)
        searchPath = DSearchPath()
        if __debug__:
            searchPath.appendDirectory(Filename.expandFrom('resources/%s' % filePath))
        else:
            searchPath.appendDirectory(Filename.expandFrom(filePath))

        found = vfs.resolveFilename(filename, searchPath)
        if not found:
            raise TileFileIOException('Unable to locate tiled file \"%s\"; File not found on %s' % (fileName, searchPath))

        self.__fileData = json.loads(vfs.readFile(filename, 1))
        self.__verifyData()

        self.__layers = self.__fileData['layers']

    def getFilePath(self):
        return self.__filePath

    def getFileName(self):
        return self.__fileName

    def getFileData(self):
        return self.__fileData

    def getWidth(self):
        return self.__fileData['width']

    def getHeight(self):
        return self.__fileData['height']

    def getSize(self):
        return (self.getWidth(), self.getHeight())

    def getTileWidth(self):
        return self.__fileData['tilewidth']

    def getTileHeight(self):
        return self.__fileData['tileheight']

    def getTileSize(self):
        return (self.getTileWidth(), self.getTileHeight())

    def getOrientation(self):
        return self.map_orientations.getString(self.__fileData['orientation'])

    def getLayers(self):
        return self.__layers

    def getProperties(self):
        return self.__fileData['']

    def __verifyData(self):
        fields = [
            'width', 'height', 'tilewidth', 'tileheight', 'orientation', 'layers', 'tilesets',
            'renderorder', 'properties', 'nextobjectid']

        for field in fields:
            if field not in self.__fileData:
                raise TileFileException('Unable to verify Tiled file %s; Missing required field \"%s\"!' % (self.__fileName, field))

        properties = [
            'MapType'
        ]

    def __str__(self):
        arguments = {
            'filePath': self.__filePath, 
            'sep': os.sep,
            'fileName': self.__fileName,
            'data': self.__fileData}
        return '%(filePath)s%(sep)s%(fileName)s\n%(data)s' % arguments

if __name__ == '__main__':
    tiled = TiledFile('tests', 'exampleDesert.json')
    print(str(tiled))
