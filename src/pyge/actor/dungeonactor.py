#=================================================================================================
#
#
#
#=================================================================================================
from actor import Actor

import pygame
from pygame.color import Color as Colors

from matrix.vector import Vector
#=================================================================================================
class TileActor(pygame.sprite.Sprite):
  """
    Actor for tiles,
  """
  def __init__(self,size, texture, image=None):
    """
      
    """
    super(TileActor,self).__init__()

    self.size = Vector( size )

    self.color = Colors("black")
    self.width = 1
    
    #self._textureid = 
    self.image_file = image #"/home/lorin/projects/ge/art/planetcute/Stone Block.png"
    self.base_image = pygame.image.load(self.image_file).convert_alpha() #image with no rotation
    self.image = pygame.transform.scale(self.base_image,(101,171))

    self.rect = pygame.Rect(0,0,self.size[0],self.size[1])

  def draw( self, screen, pos ):
    """
      draws the tile on screen
    """
    pos = (pos[0]-self.size[0]/2, pos[1]-self.size[1]/2)
    screen.blit(self.image, pos)
    self.rect  = pygame.Rect(pos[0],pos[1]+50,self.size[0],self.size[1])
    #pygame.draw.rect( screen, self.color, self.rect, self.width )
#=================================================================================================
#class DungeonActor():
#=================================================================================================
