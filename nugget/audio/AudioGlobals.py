"""
 * Copyright (C) The Project "Nugget" Team - All Rights Reserved
 * Written by Jordan Maxwell <jordanmax@nxt-studios.com>, May 2nd, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
 """

from direct.showbase.PythonUtil import Enum

MusicTypes = Enum('PRIMARY, SECONDARY, COMBAT')

AudioBasePath = 'audio/'

HELLO = '%shello.mp3' % AudioBasePath # TESTING AUDIO ONLY. DO NOT USE