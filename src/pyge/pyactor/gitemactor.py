#=================================================================================================
# Gitem Actor
#=================================================================================================
from actor import Actor
import pygame
from pygame.color import Color as Color
#=================================================================================================
class GitemActor(Actor):
  def __init__(self):
    self.color  = Color("black")
    self.radius = 3
    self.width  = 2
    self.pos    = (0,0)
  def draw(self,surface,pos):
    pos = ( pos[0]+50 , pos[1]+40 )
    pygame.draw.circle( surface, self.color, pos , self.radius, self.width  )
