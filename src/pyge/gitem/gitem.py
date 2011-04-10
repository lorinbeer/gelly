#=================================================================================================
#  Game Item Class
#    represents an in game item
#
#=================================================================================================
import sys
sys.path.append("/home/lorin/projects/gelly/objs")
from actor import Actor
#=================================================================================================


class Gitem( Actor ):
  """
    Represents in game items
  """
  default_model = [ (0,0), (0,50), (50,50), (50,0) ]
  def __init__( self, **kwargs ):
    """
      volume - the volume this object occupies
    """

#    super( Gitem, self ).__init__(kwargs.get('model',Gitem.default_model),
#                                  kwargs.get('texture',None),
#                                  kwargs.get('drawmode','polygon'),
#                                  kwargs.get('offset',(0,0) )
    self.texture = kwargs.get('texture',None)
    if self.texture:
      super( Gitem, self ).__init__(self.texture)

    self.type = None
    self.name = 'item name'
    self.value = None
    self.volume = 1.0
    self.mass   = 1.0
    self._slot = None
  def draw(self,pos):
    if self.texture:
      pos[1]+=0.016
      super( Gitem, self ).draw(pos)
    
  def __str__(self):
    """
    """
    return 'item: %(name)s' %{'name':self.name}


class GitemFactory( object ):
  """
  """
  def makegitem(self):
    """
    """
    gitem = Gitem()
    gitem.name = 'Short Sword'
    gitem.value = 10.0
    gitem.type = 'weapon'
    gitem._basedamage = 10
    gitem._reach = 0.3 #m
    gitem._slot = 'rhand'
    gitem._mass = 0.50
    gitem._coverage = 0.0
    #physical stats


    #weapon stats
    gitem._parry = True #TODO: parry rating

    return gitem
