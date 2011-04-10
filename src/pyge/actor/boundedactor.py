#=================================================================================================
# Bounded Actor Class
#
#
#
#
# Lorin Beer
# 
#=================================================================================================

from actor import Actor
from rectangle import Rectangle

#=================================================================================================
#TODO:
#  - singleton gfx
#  - singleton dispatcher
#  - be able to pass Actor constructor id's 
#=================================================================================================

class BoundedActor( Actor ):
  """
    Actor class with bounding rectangle
  """
  def __init__( self, **kwargs ):
    """

      Keyword Arguments: 
        - model: 
        - texture: 
        - drawmode: 
        - rectdim: 
        - boundoffset: (x,y) offset of bounding rectangle from (0,0) in model coordinates, used
                       to position the bounding rectangle within the actor model
      
      self, model, texture=None, drawmode='polygon'
    """
    try:
      texture  = kwargs.get( 'texture', None )
      drawmode = kwargs.get( 'drawmode', 'polygon' )
      self._boundoffset = kwargs.get( 'boundoffset', (0,0) )
      super(BoundedActor,self).__init__( kwargs['model'], texture, drawmode )

      self._bound = Rectangle( **kwargs )
    except KeyError:
      print "Bounded Actor requires a model"
#=================================================================================================
  def draw( self, pos, name,drawbound=False ):
    """
    """
    super(BoundedActor,self).draw(pos,name)
    if drawbound: self._bound.draw((pos[0]+self._boundoffset[0],pos[1]+self._boundoffset[1]),name)
    else: self._bound.updatepos( (pos[0]+self._boundoffset[0],pos[1]+self._boundoffset[1]) )
#=================================================================================================
  def collide(self,point):
    """
    """
    return self._bound.collide(point)
