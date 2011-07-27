#=================================================================================================
#  pyactor effect Class
#    animated actor class responsible for handling graphic objects with no associated game item
#  
#
#
#=================================================================================================
import os
import sys
sys.path.append("/home/lorin/projects/gelly/objs")
from actor import Animactor, Vertel
#=================================================================================================
#How it works
#  Effect class is an animactor as well as a node class
#  Effect has a dict of triggers
#    dict keys are frames, on that frame, execute the list associated with the key
#    on death, all unexecuted children are executed
#  position is important, we should store it as a 
#=================================================================================================
class Node(object):
  """
    lightweigt node class 
  """
  def init(self,parent,children,data):
    """
      @param parent    node to be this nodes parent, will add itself as a child of parent on init
      @param children  list of nodes
    """
    try:
    #check that parent is a valid node
      if not parent:
        self._isroot = True
      else:
        self._isroot = False
        self._parent = parent
        parent.addChild( self )
      self._children = set()
      for child in children:
        self._children.add(child)
    except AttributeError:
      print "Error: either parent or child nodes are not valid node objects"
  #=========================================================================================================================
  def addChild(self,child):
    """
    """
    self._children.add(child)
    child._parent = this
  #=========================================================================================================================
  def removeChild(self,child):
    """
      @param child  the child to remove from the tree
    """
    if child in self._children:
      self._children.remove(child)
  #=========================================================================================================================
  def detach(self):
    """
      detach the branch rooted at this node
      if this node already is a root, does nothing
    """
    if not self._isroot:
      self._parent.pop(self)
      self._parent = None
#===========================================================================================================================
#
#===========================================================================================================================
class EffectNode(Node):
  """
  """
  #=========================================================================================================================
  def init(self):
    """
    """
  #=========================================================================================================================
  def execute(self):
    """
    """
#===========================================================================================================================
#graphics system gets a sing
#graphics system gets passed a tree structure to execute
#

#=================================================================================================
class Effect( Animactor ):
  """
  """
  def __init__( self, assetpath ):
    """
      Initialize the Effect with the art assets located at assetpath

      INPUT:
        assetpath: the full path to the directory containing the images to use
      
      image file names should be sortable in the order they are to be played
    """
    #TODO: hardcoded asset paths
    self._gfxeffects={'null' : None,
                      'slash': { 'assetpath' :"/home/lorin/projects/ge/art/cut_a",
                                 'framepaths': [] }
                     }
    framenames = os.listdir( assetpath ) #retrieve the names of all files in the dir
    framenames.sort()
    framepaths = []
    for frame in framenames:
      framepaths.append( str( os.path.join( assetpath, frame )) )#generate the full path to the asset

    #TODO: BAAAAH, MESSY, model should be somewhere else, like file or db
    _model = Vertel()
    _model.set( [ ( 0.0, 0.0, 0.0 ), 
                  ( 0.0, 100.0/600.0, 0.0 ), 
                  ( 100.0/800.0, 100.0/600.0,0.0 ),
                  ( 100.0/800.0 , 0.0, 0.0 ) ] )
    super( Effect, self ).__init__( framepaths, _model )
    self.alive = True


    #init triggers
    self._triggers = {} #currently 1 callback per frame, multiple triggers doable with multidict

  #===============================================================================================
  def draw( self, pos ):
    """
    """
    super( Effect, self ).draw(pos)
    if self.done: self.alive = False
    #part of prototype trigger system
    if self.currentframe in self._triggers:
      self._triggers[self.currentframe].call()

  #===============================================================================================
  def reset(self):
    """
    """
    self.done  = False
    self.alive = True
  #===============================================================================================
  def attachtrigger(self, frame, trigger):
    """
      prototype trigger system
    """
    self._triggers[frame] = trigger
#=================================================================================================
