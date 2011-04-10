#=================================================================================================
# Rectangle Class
# 
#
#
#
# Lorin Beer
# 
#=================================================================================================

from graphics import Graphics
from actor import *

#=================================================================================================
#
#
#=================================================================================================
class Rectangle( Actor ):
  """
  """
  def __init__( self, **kwargs ):
    """

      KEYWORD INPUT:
            x     : width, default 100 units
            y     : height, default 100 units
    """
    self._x = kwargs.get('x',100)
    self._y = kwargs.get('y',100)
    self._width = kwargs.get('width',1.0)
    self._mode = kwargs.get('mode','lines')
    #self._c = center
    self._model = self.__generatemodel__( self._x, self._y )
    super(Rectangle,self).__init__( self._model, None, 'lineloop' )

  
  #===============================================================================================
  def __generatemodel__(self,x,y):
    """
      generate a model for this object
    """
    return [ (0,0), (0,self._y), (self._x,self._y), (self._x,0) ]
  #===============================================================================================
  def __generatetrans__(self):
    """
      generate main diagonal entries of transformation matrix
    """
    self._transform = [ (), (), (0,0) ]
  #===============================================================================================
  def collide( self, point ):
    """
    """
    self._position
    self._x
    self._y
    if point[0] > self._position[0] and point[0]<(self._position[0]+self._x) and\
       point[1] > self._position[1] and point[1]<(self._position[1]+self._y):
      return True
    return False
  #===============================================================================================

  #===============================================================================================
