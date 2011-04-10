#=================================================================================================
# AnimatedActor Class
#
#
#=================================================================================================

import os
from graphics import Graphics
from actor import Actor
import pygame

#=================================================================================================

class AnimatedActor( Actor ):
  """
  """
  def __init__(self, asset_path, fps, loc):
      """
        asset_path: the full path to the directory containing the art assets for this animation
      """
      model = [ (0,0), (0,100), (100,100), (100,0) ]
      super(AnimatedActor,self).__init__( model )
      gfx = Graphics()
      self._textures = list()
      image_names = os.listdir(asset_path)
      image_names.sort()
      for each in image_names:  
        path = os.path.join( asset_path, each ) #use path.join to insure cross platform
        self._textures.append( gfx.texture_register(path) )#register the texture with the graphics

        #we need to scale, and the scale factor needs to come from somewhere
#      for i,v in enumerate(self.images):
#        self.images[i] = pygame.transform.scale(v,( v.get_height()/3, v.get_width()/3    ))


      # Track the time we started, and the time between updates.
      # Then we can figure out when we have to switch the image.
      self._start = pygame.time.get_ticks()
      self._delay = 1000 / fps
      self._last_update = 0
      self._frame = 0

        # Call update to set our first image.
      self.update(pygame.time.get_ticks())
      self.loc = loc

      self.alive = True
      self.repeat = False
      
  def update(self, t):
        # Note that this doesn't work if it's been more that self._delay
        # time between calls to update(); we only update the image once
        # then, but it really should be updated twice.
      #if t - self._last_update > self._delay:
      self._frame += 1
      if self._frame >= len(self._textures):
#          if self.repeat:
#            self._frame = 0
#          else:
        return False
      self._texid = self._textures[self._frame]
      self._last_update = t
      return True

