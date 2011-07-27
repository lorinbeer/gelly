#===========================================================================================================================

#===========================================================================================================================
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
