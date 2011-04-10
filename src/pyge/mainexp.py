#!/usr/bin/python

import gutil
import pygame
from pygame.locals import *
from OpenGL.GL import *


def main():
    pygame.init()
    gutil.initializeDisplay(800, 600)

    glColor4f(1.0,1.0,1.0,1.0)

    done = False

    cowTex, w, h = gutil.loadImage('art/planetcute/Character Boy.png')
    cow = gutil.createTexDL(cowTex, w, h)
    alienTex, w, h = gutil.loadImage('art/alien.png')
    alien = gutil.createTexDL(alienTex, w, h)

    while not done:
        glLoadIdentity()
        glTranslatef(100, 100, 0)
        glCallList(cow)
        glTranslatef(400, 400, 0)
        glCallList(alien)

        pygame.display.flip()

        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == QUIT \
               or event.type == KEYDOWN and event.key == K_ESCAPE:
                done = True

if __name__ == '__main__':
    main()
