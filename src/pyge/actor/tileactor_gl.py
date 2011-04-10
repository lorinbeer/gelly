#=================================================================================================
# Class TileActor_gl.py
#
#
#
#=================================================================================================

from pydispatch import dispatcher

from matrix.vector import Vector

from graphics import Graphics

#=================================================================================================

#class Rect(object):
#  """
#  """
#  def __init__(self,width,height,

#=================================================================================================
class TileActor_gl( object ):
  """
  """
  def __init__( self, size, texturepath, gfx_sys ):
    """
    """

    self.size = Vector( size )
    self._gfxsys = gfx_sys
    self._texpath = texturepath
    self._texid = self._gfxsys.texture_register( self._texpath )
#=================================================================================================
  def draw( self, pos ):
    """
      Request that this object be drawn at pos
    """
    self._gfxsys.blit( self._model, self._texid, pos)
#=================================================================================================
  def __del__(self):
    """
    TODO: call graphics system to free 
    """
    print "free tile actor"
#=================================================================================================
