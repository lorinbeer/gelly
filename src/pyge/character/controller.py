#=================================================================================================
# Controller class
#
#  
#=================================================================================================
 #pygame includes
import sys
sys.path.append("/home/lorin/projects/gelly/objs ")
from actor import Actor
from actor import Vertex
from pysdlutil import SDLKey, SDL_EventType, Event


from character import Character
from action import Action, Action_Type


from matrix.vector import Vector
from other.euclid import Vector2
#=================================================================================================
class Selection( Actor ):
  """
  """
  def __init__(self):
    """
    """
    self.sel = False
    self._image_file = "/home/lorin/projects/ge/art/planetcute/Selector.png"
    self._pos = Vertex()
    self._pos.append( -1.0 )
    self._pos.append( -1.0 )
    super( Selection, self ).__init__( self._image_file )#, offset=(0,50))
  #===============================================================================================
  def select(self, tile_actor ):
    """
    """
    npos = tile_actor.getpos()
    self._pos[0] = npos[0]+tile_actor._itemoffset[0]
    self._pos[1] = npos[1]+tile_actor._itemoffset[1]+0.02
    self.sel = tile_actor
  #===============================================================================================
  def draw(self):
    """
    """
    if self.sel:
      npos = self.sel.getpos()
      self._pos[0] = npos[0]+self.sel._itemoffset[0]
      self._pos[1] = npos[1]+self.sel._itemoffset[1]+0.02
      super(Selection,self).draw(self._pos)
#=================================================================================================
#=================================================================================================


#=================================================================================================
#=================================================================================================
class Controller(object):
  """
    Controller Class
      Acts as the interface between the user and an associated character object, interpreting
      events and returning Actions
  """
  def __init__(self, character ):
    """
      character - the character object that this Controller is associated with
    """
    #will load command settings from a file
    self._character = character
    self._selection = Selection()
  #===============================================================================================
  def interpret(self, event, dungeon ):
    """
      interpret the event in terms of the associated character object, returning an action which
      can be used to apply the desired effect to the game state
    """
    if event.type == SDL_EventType.KEYUP:
      return self.interpretkeyevent(event,dungeon)
    elif event.type == SDL_EventType.MOUSEBUTTONUP:
      return self.interpretmouseevent(event,dungeon)
    return False
  #===============================================================================================
  def interpretkeyevent(self, keyevent, dungeon):
    """
    """
    if keyevent.type == SDL_EventType.KEYUP:
      direc = False
      #===========================================================================================
      # direction keys, directely interpreted as move actions
      #===========================================================================================
      if keyevent.key == SDLKey.SDLK_UP:
         direc = Vector2(0,-1)
      elif keyevent.key == SDLKey.SDLK_DOWN:
        direc = Vector2(0,1)
      elif keyevent.key == SDLKey.SDLK_RIGHT:
        direc = Vector2( 1,0)
      elif keyevent.key == SDLKey.SDLK_LEFT:
        direc = Vector2(-1,0)
      #===========================================================================================
      
      #==========================================================================================
      elif keyevent.key == SDLKey.SDLK_a:
        self._character.mind.qaction.append ( Action( verb  = Action_Type['attack'],
                                                     actor = self._character,
                                                     target= self._character.target,
                                                     stage = dungeon ) )

#      elif keyevent.scancode == 33: #p key
 #       loc = dungeon.loc(self.character)
 #       self.character.mind.qaction.append( Action( verb  = Action_Type['grab'],
                 #                                   stage = dungeon,
                 #                                   actor = self.character,
                 #                                   tile  = loc ) )
#      elif keyevent.scancode == 32: #o key
#        loc = dungeon.loc(self.character)
#        self.character.mind.qaction.append( Action( verb  = Action_Type['drop'],
                     #                       stage = dungeon,
                     #                       actor = self.character ) )
    if  direc:
      self._character.mind.qaction.append( Action( verb = Action_Type['move'],
                                          stage = dungeon,
                                          actor = self._character,
                                          target = direc) )
    return False
  #===============================================================================================
  def interpretmouseevent(self, mevent, dungeon ):
    """
      
    """
    if mevent.type == SDL_EventType.MOUSEBUTTONUP:
      self._selection.select( dungeon.map[mevent.x, mevent.y] )
