#=================================================================================================
# Inventory Class
#  
#
#=================================================================================================

from gitem.gitem import Gitem

#=================================================================================================

class Inventory( list ):
  """
  """
  def __init__(self, volume):
    """
    """
    #TODO check type for volume
    super(Inventory,self).__init__()
    self.volume = volume
    self.maxvolume = 50.0

  def __getitem__(self,key):
    """
      implements self[key] 
    """
    return super(Inventory,self).__getitem__(key)


  def __setitem__(self,key,value):
    """
      implements self
    """
    #TODO check that new item can fit in the inventory
    return super(Inventory,self).__setitem__(key,value)
  

  def append(self, x):
    """
      implements list.append(x), with a volume check
    """
    try:
      if self.volume + x.volume <= self.maxvolume:
        super(Inventory,self).append(x)
    except TypeError:
      print "type error, x must be of type gitem"

    


