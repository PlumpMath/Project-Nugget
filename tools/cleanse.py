#!/usr/bin/env python2
"""
 * Copyright (C) Stellar Gaming Network - All Rights Reserved
 * Written by Jordan Maxwell <jordanmax@nxt-studios.com>, April 19th, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
 """


import os
import sys
import shutil
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', default='../', help='Folder to cleanse')
    args = parser.parse_args()

    if not os.path.exists(args.folder):
        print('%s does not exist! Exiting..' % args.folder)
        sys.exit()

    print ('Cleansing %s...' % os.path.abspath(args.folder))
    for root, dirs, filenames in os.walk(args.folder):
        for folder in dirs:
            if folder == '__pycache__':
                print('Removing %s..' % folder)
                shutil.rmtree(os.path.join(root, folder))

        for filename in filenames:
            if filename.endswith('.pyc'):
                print('Removing %s...' % filename)
                os.unlink(os.path.join(root, filename))

    print('Done!')
