#=================================================================================================
# Character Actor
#=================================================================================================
from actor import Actor
import pygame
from pygame.sprite import Sprite
from pygame.color import Color as Color
#=================================================================================================
class CharacterActor(Sprite):
  def __init__(self, image_file):
    super(CharacterActor,self).__init__()

    self.base_image = pygame.image.load(image_file).convert_alpha() #image with no rotation
    self.image = pygame.transform.scale(self.base_image,(101,171))

    self.color  = Color("black")
    self.radius = 12.5
    self.width  = 1
    self.pos    = (0,0)
    print self.color
  def draw(self,surface,pos):
    #pygame.draw.circle( surface, self.color, pos , self.radius, self.width  )
     #       draw_pos = self.image.get_rect().move(
     #       self.pos.x - self.image_w / 2, 
     #       self.pos.y - self.image_h / 2)
    pos = (pos[0] , pos[1]-85 )
    surface.blit(self.image, pos)
