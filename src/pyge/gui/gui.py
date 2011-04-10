#=================================================================================================
# GUI System
#
#
#
#=================================================================================================

from OpenGL.GL import *

import random

from pydispatch import dispatcher

#=================================================================================================
class GuiSystem(object):
  """
  """
  def __init__(self):
    """
    """
    self.containers = []
    actionbar = Container( (0,0), 400, 100 )

    def colourflip(but):
      print 'fuck yeah'
      if but._colour[0] == 1.0:
        but._colour = [0.0, 1.0, 1.0]
      else:
        but._colour = [1.0, 0.0, 0.0]
      but.__createcalllist__(but._pos,but._width,but._height)

    but1 = Button( (0,0), 100, 100 )
    but1.registercallback(colourflip,but1)
    but2 = Button( (100,0), 100, 100 )
    but2.registercallback(colourflip,but2)
    but3 = Button( (200,0), 100, 100 )
    but3.registercallback(colourflip,but3)
    but4 = Button( (300,0), 100, 100 )
    but4.registercallback(colourflip,but4)


    
    actionbar.addwidget(but1, (0,0) )
    actionbar.addwidget(but2, (100,0) )
    actionbar.addwidget(but3, (200,0) )
    actionbar.addwidget(but4, (300,0) )
  
    self.containers.append(actionbar)
  #===============================================================================================
  def processevent(self,event):
    """
    """
    #currently, can only process events with pos attribute
    try:
      event = (event.pos[0],600-event.pos[1])
      for each in self.containers:
        if each.intersect(event):
          return True
    except AttributeError:
      return False
  #===============================================================================================
  def draw(self):
    """
    """
    for each in self.containers:
      each.draw()
  #===============================================================================================
  
#=================================================================================================



#=================================================================================================
class Widget(object):
  """
  """
  def __init__(self, pos, width, height):
    """
      pos    - 2D tuple representing top left corner of the button
      length - 
      width  -
    """
    self._pos    = pos
    self._width  = width
    self._height = height
  #===============================================================================================
  def intersect(self,coord):
    """
      intersect a point at coord with this widget
      coord - indexable
    """
    print 'coord', coord
    print 'pos', self._width, self._height 
    if coord[0] > self._pos[0] and coord[0] < self._pos[0]+self._width and coord[1] > self._pos[1] and coord[1] < self._pos[1]+self._height:
      return True
    return False
  #===============================================================================================

#=================================================================================================
# TODO 
#  - should act like an iterator
#  - auto stacking algorithm
#  - maybe this should render to a texture, updated as neccesary
class Container(Widget):
  """
    
  """
  def __init__(self, pos, width, height):
    """
      
    """
    super(Container,self).__init__(pos,width,height)
    self._contents = list()
  #===============================================================================================
  def addwidget(self, widget, pos):
    """
      add a widget to the container
      widget: widget to add
      pos   : position to add the widget, relative to self's border
    """
    #TODO: check pos
    widget.setposition( (pos[0]+self._pos[0],pos[1]+self._pos[1]) )
    self._contents.append( widget )
  #===============================================================================================
  def draw(self):
    """
    """
    for each in self._contents:
      each.draw()
  #===============================================================================================
  def intersect(self,coord):
    """
    """
    if super(Container,self).intersect(coord):  #if the intersection hits
      print "container intersected"
      for each in self._contents:
        if each.intersect(coord):
          return True #first widget in the container to register a hit
    return False
    
#=================================================================================================




#=================================================================================================
class Button(Widget):
  """
  
  """
  def __init__(self, pos, width, height):
    """
      pos    - 2D tuple representing top left corner of the button
      length - 
      width  -
    """
    super(Button,self).__init__(pos,width,height)
    self._colour = [ 1.0, 0.0, 0.0 ]
    self.__createcalllist__(pos,width,height)
  #===============================================================================================
  def __createcalllist__(self,pos,width,height):
    """
    """
    self._lid = random.randint( 0, 1000 ) #generate a 'unique' list id

    glNewList(self._lid,GL_COMPILE)
    glColor3f(self._colour[0],self._colour[1],self._colour[2])
    glBegin(GL_POLYGON)
    glVertex3f( pos[0], pos[1], 0.0)
    glVertex3f( pos[0]+width, pos[1], 0.0)
    glVertex3f( pos[0]+width, pos[1]+height, 0.0)
    glVertex3f( pos[0], pos[1]+height, 0.0)
    glEnd()
    glColor3f(0.0,0.0,0.0)
    glLineWidth(10.0)
    glBegin(GL_LINE_LOOP)
    glVertex3f( pos[0], pos[1], 0.0)
    glVertex3f( pos[0]+width, pos[1], 0.0)
    glVertex3f( pos[0]+width, pos[1]+height, 0.0)
    glVertex3f( pos[0], pos[1]+height, 0.0)
    glEnd()
    glColor3f(1.0,1.0,1.0)
    glEndList()
  #===============================================================================================
  def setposition(self,pos):
    """
    """
    glDeleteLists(self._lid,1)
    self.__createcalllist__(pos,self._width,self._height)
  #===============================================================================================
  def callback(self):
    self._callback(self._callbackargs)
  #===============================================================================================
  def registercallback(self,function,argdict):
    """
    """
    self._callback     = function
    self._callbackargs = argdict
  #===============================================================================================
  def draw(self):
    """
    """
    glCallList(self._lid)
  #===============================================================================================
  def intersect(self,coord):
    """
      intersect the coord with this widget
 
      if it hits, activate this button's callback and return True
    """
    if super(Button,self).intersect(coord):
      self.callback()
      return True
    return False

#=================================================================================================
