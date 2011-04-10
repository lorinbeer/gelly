#=================================================================================================
# Class Graphics
#
#
#
#=================================================================================================
from PIL.Image import open
import pygame 
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import copy
#=================================================================================================
#TODO:
# - BLIT: - only half implemented 
#         - needs a much more elegant way of clearing the screen
#         - actors need an id, identifying their drawlist, so an actor, on death, can remove
#           itself from the drawlist
#         - when blitting, we must redraw the area of the streen that the actor was on, as well
#           as well as where the actor will be, this requires more complex architecture, possibly
#           an intermediate screen representation (surface)
# - Drawing: - opengl 4.0 compliance
#=================================================================================================

G_DEFAULT_PLATFORM = 'linux'

#class Rect(object):

# def __init__(self, ):

# def 

#=================================================================================================
from other.singleton import Singleton
class Graphics(object):
  """
  """
  draw_mode = {'polygon'  : GL_POLYGON, 
               'lines'    : GL_LINES, 
               'linestrip': GL_LINE_STRIP,
               'lineloop' : GL_LINE_LOOP }
  __metaclass__ = Singleton
  def __init__(self,**kwargs):
    """
      INPUT:
       (kwargs)-'redraw': True/False clear screen and redraw every frame
                          static screen games should be false
    """
    print "init graphics"
    self._w = 800
    self._h = 600
    self._textures = {}
    pygame.display.set_mode((self._w,self._h), pygame.OPENGL|pygame.DOUBLEBUF)
    self._drawlist = []
    self._olddraw = []
    self.__initgl__( self._w,self._h )
    if 'redraw' in kwargs:
      self._redraw = kwargs['redraw']
#=================================================================================================
  def __initgl__( self, w, h ):
    """
    """
#   glutInit(sys.argv)
#   glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
#   glutInitWindowSize(800,600)
#   glutCreateWindow('')

    glClearColor(0.0, 0.0, 0.0, 1.0)
    #glClearColor(0.0f, 0.0f, 0.0f, 0.5f);
    glShadeModel(GL_SMOOTH)
    #glEnable(GL_CULL_FACE)
    #glEnable(GL_DEPTH_TEST)
    #glEnable(GL_LIGHTING)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, w, 0, h);
    glMatrixMode(GL_MODELVIEW);

    #set up texturing

    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    #glutDisplayFunc(self.display)

    self.textureid = self.__loadimage__()
    #self._drawlist.append( self.__createTexCL__(self.textureid, (80,80),(40,40)) )

    return


#=================================================================================================
  def __loadimage__( self, filepath='/home/lorin/projects/ge/art/alien.png' ):
    """
    """
#    print filepath
    img = open( filepath )
    img_data =  img.tostring("raw", "RGBA", 0, -1) 
    #numpy.array( list( img.getdata() ), numpy.int8)
    texture_id = glGenTextures(1)
    glPixelStorei( GL_UNPACK_ALIGNMENT, 1 )
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, 
                  img.size[0], 
                  img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data )
    self._textures[filepath] = texture_id
    return texture_id
#=================================================================================================
  def __createQuadCL__(self, model, pos, texture_id=None, mode='polygon' ):
    """
      PRIVATE: if you want to register a new texture with Graphics, go through texture_register
      Compiles an openGL call list, returning the call list id

      INPUT:
    """
    tc = [ (0,0), (0,1), (1,1), (1,0) ]
    newList = glGenLists(1)
    glNewList(newList,GL_COMPILE)
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()
    glTranslatef( pos[0], pos[1], 0)
    glEnable (GL_BLEND); glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    if texture_id:
      glEnable(GL_TEXTURE_2D) #enable 2d texturing for the duration of the list
      glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin( Graphics.draw_mode[mode] )
    for i in range(0,len(model)):
      if texture_id: glTexCoord2fv( tc[i] )
      glVertex2fv( model[i] )
    glEnd()
    if texture_id: glDisable(GL_TEXTURE_2D)
    glLoadIdentity()
    glEndList()

    return newList
#=================================================================================================
  def begin(self):
    glutMainLoop()
#=================================================================================================
  def display(self):
    """
    """
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    
    for entry in self._drawlist:
      glCallList( entry['cl'] )

    #glutSwapBuffers()

    self._olddraw = self._drawlist[:]
    self._drawlist = []
    return

#=================================================================================================
  def texture_register( self, texturepath ):
    """
      Register a texture with the Graphics system, returning a unique integer id.

      If the texture has already been registered, returns the id without reloading unless reload
      is specified as an argument.
    """
    return self._textures.setdefault( texturepath, self.__loadimage__( texturepath ) )
#=================================================================================================
  def blit( self, model, pos, name, texid=None, mode='polygon' ):
    """
      Draw a rectangle at pos with texture corresponding to texid.
      
      If doublebuffering is enabled, blit will immediately perform the draw onto the backbuffer
      If doublebuffering is disabled, blit will be performed on the next call to draw
    """
    self._drawlist.append( {'name':name, 'cl':self.__createQuadCL__(model, pos, texid, mode)} )
#=================================================================================================
  def select( self, point ):
    """
    """
    glInitNames( )
    glPushName( 0 )
    glSelectBuffer ( 64 )

    viewport = glGetIntegerv( GL_VIEWPORT ) 
    glMatrixMode( GL_PROJECTION )

    glPushMatrix()
    glLoadIdentity()
    gluPickMatrix( point[0], viewport[3] - point[1], 1, 1, viewport ) 
    gluOrtho2D(0, self._w, 0, self._h)
    glRenderMode( GL_SELECT )

    glPushName( -1 )
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    print "old draw ", len(self._olddraw)
    for i,entry in enumerate(self._olddraw):
      glLoadName( i )
      glCallList( entry['cl'] )

    glMatrixMode( GL_PROJECTION )
    glPopMatrix()
    glLoadIdentity()
    gluOrtho2D(0, self._w, 0, self._h)

    buffer = glRenderMode( GL_RENDER )

    out = []
    for hit_record in buffer:
      #print "hit record:", hit_record.names[0]
      print "tile hit: ",self._olddraw[ hit_record.names[0] ]['name']
      out.append( self._olddraw[ hit_record.names[0] ]['name'] )
    return out

#=================================================================================================

if __name__ == "__main__":
  g = Graphics()

#=================================================================================================

#=================================================================================================
