#=================================================================================================
# Actor Class
#  Base Actor Class
#
#
#
# Lorin Beer
# 
#=================================================================================================

from graphics import Graphics

#=================================================================================================
#TODO:
#  - singleton gfx
#  - singleton dispatcher
#  - be able to pass Actor constructor id's 
#=================================================================================================

class Actor( object ):
  """
    Base Class for Actors. Actors are any objects with an onscreen representation.

    Actor class contains:
     model    : wireframe model representing the onscreen actor
     rectangle: bounding rectangle, projection of model on to the plane, used for intersection 
                and collision detection            
     texture  : image to texture the model
  """
  def __init__( self, model, texture=None, drawmode='polygon', offset=(0,0) ):
    """
      Initialize the actor
      INPUT:
            - model: unknown representation of this Actor's model, dependent on graphics system
            - texture: unknow representation of the texture to apply to this Actor's model
            - bounding_rect: rectangular projection of this actor's model onto the plane, used
                             for intersection and collision
            - gfx_sys: graphics system reference TODO: get rid of this
    """
    self._model = model #TODO assume array
    #self._boundrect = bounding_rect #TODO assume array
    self._texpath = texture #TODO assume path
    self._mode = drawmode
    self._gfxsys = Graphics()
    self._offset = offset
    if texture: 
      self._texid = self._gfxsys.texture_register( self._texpath )
    else:
      self._texid = None
    self._position = (0,0)
#=================================================================================================
  def draw( self, pos, name ):
    """
      Request that this object be drawn at pos
    """
    self._position = (pos[0]+self._offset[0],pos[1]+self._offset[1])
    #print self._position
    self._gfxsys.blit( self._model, self._position, name, self._texid, self._mode )
#=================================================================================================
  def updatepos( self, pos ):
    """
      update this actor's position outside of a draw call
    """
    self._position = pos
#=================================================================================================
#  def __del__(self):
#    """
#    TODO: call graphics system to free texture and buffer arrays
#    """
#    print "free tile actor"
#=================================================================================================
