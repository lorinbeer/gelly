#=================================================================================================
import sys
import pygame
from pygame.color import Color as Colors

#import gutil
from pygame.locals import *
from OpenGL.GL import *

import sys
sys.path.append("/home/lorin/projects/ge1/dungeon")
#=================================================================================================
from dungeon.dungeon import DungeonMap, DungeonDecorator
from dungeon.dungeongenerator import DungeonGenerator
from dungeon.dungeonmaster import DungeonMaster
#
from character.character import Character
from character.action import Action,Move,Attack
from character.controller import Controller, Selection
#
from matrix.vector import Vector
from other.euclid import Vector2
#
from gui.gui import GuiSystem
#

#=================================================================================================

from pydispatch import dispatcher

#=================================================================================================

from graphics import Graphics

#=================================================================================================

pygame.init()
#pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)
#pygame.display.set_mode(SCREEN_SIZE,HWSURFACE|OPENGL|DOUBLEBUF)

size = list( (800,600) )
speed = [2, 2]
black = 0, 0, 0
#screen =  pygame.Surface( size )#pygame.display.set_mode(size)

#
clock = pygame.time.Clock()

#
gfx = Graphics()
dg = DungeonGenerator(10,64)
dungeon = dg.generate()

#
decorator = DungeonDecorator()
pc = decorator.decorate(dungeon)
selection = pc.controller.selection

dungeonmaster = DungeonMaster(dungeon)

print "character list len %(num)i"%{'num': len(dungeon.characters)}

#
update_list = list() #every frame, items in this list are updated and blitted to screen

#=================================================================================================
guisys = GuiSystem()
#=================================================================================================

#=================================================================================================
import os
path = os.path.join('home', '*.fasta') 
print path

while 1:

  timepassed = clock.tick( 10 ) #FPS
  
  loc  = dungeon.loc(pc)    #retrieve
  #===============================================================================================
  #EVENT HANDLING
  #worry about multiple commands per frame later
  for event in pygame.event.get():

    action = False
 
    ###refactor###
    if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN:
      if not guisys.processevent(event):
        action = pc.controller.interpret( event, dungeon )
    ###refactor###
      effects = dungeonmaster.turn()
      dungeonmaster.update()
#      print effects


      for effect in effects:
        if effect: update_list.append( effect )


    elif event.type == pygame.QUIT:
      sys.exit()
  #===============================================================================================
  #draw calls


  loc = dungeon.loc(pc)
  dungeon.draw( loc )
  selection.draw()

  for each in update_list:
    each.draw( each.loc, None )
    if not each.update( pygame.time.get_ticks() ):
      update_list.remove(each)

  gfx.display()

  pygame.display.flip()


  #===============================================================================================

#  textureData = pygame.image.tostring(screen, "RGBA", 1)
#  width  = screen.get_width()
#  height = screen.get_height()

#  texture = glGenTextures(1)
#  glBindTexture(GL_TEXTURE_2D, texture)
#  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
#  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
#  glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,textureData)


#  tex, w, h = gutil.loadImage('art/planetcute/Character Boy.png')
#  foo = gutil.createTexDL(texture, width, height)


#  glLoadIdentity()
  #glTranslatef(100, 100, 0)
#  glCallList(foo)
#  guisys.draw()
  #===============================================================================================

#  pygame.display.flip()

#=================================================================================================
