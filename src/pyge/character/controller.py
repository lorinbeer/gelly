#=================================================================================================
# Controller class
#
#  
#=================================================================================================
 #pygame includes
import sys
sys.path.append("/home/lorin/projects/gelly/objs ")
from actor import Actor, Vertel
from actor import Vertex
from pysdlutil import SDLKey, Gelly_EventType, Event

from character import Character
from action import Action
from skill import Skill, SkillFactory

from util.vector import Vector

import ast
#=================================================================================================


#=================================================================================================
#=================================================================================================
def setskillcb():
  print "setskill cb"
  return "{ nightmare:ride }"

#=================================================================================================
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
    _model = Vertel()
    _model.set( [ ( 0.0, 0.0, 0.0 ), 
                  ( 0.0, 171.0/600.0, 0.0 ), 
                  ( 101.0/800.0, 171.0/600.0,0.0 ),
                  ( 101.0/800.0 , 0.0, 0.0 ) ] )
    _bound = Vertel()
    _bound.set( [ ( 0.0, 0.0, 0.0 ),
                  ( 0.0, 100.0/600, 0.0 ),
                  ( 100.0/800.0, 100.0/600, 0.0 ),
                  ( 100.0/800, 0.0, 0.0 ) ] )
    super( Selection, self ).__init__( self._image_file, _model, _bound )#, offset=(0,50))
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

#Messages
#  the controller can receive string messages encoding some manipulation of the game state
# Actionbar Messages
#  target action bar, and instruct the character to execute the designated action
#
#    actionbar:execute:<int>
#    actionbar:slotchange:<int>
#    actionbar:skillchange:<int>

#Return Messages

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
    self.character = character
    self._selection = Selection()
    self._jscallbackdict = {'setskill':setskillcb}
  #===============================================================================================
  def interpret(self, event, dungeon ):
    """
      interpret the event in terms of the associated character object, returning an action which
      can be used to apply the desired effect to the game state
    """
    if event.type == Gelly_EventType.MSGEVENT: print event.message
    if event.type == Gelly_EventType.KEYUP:
      return self.interpretkeyevent(event,dungeon)
    elif event.type == Gelly_EventType.MOUSEBUTTONUP:
      return self.interpretmouseevent(event,dungeon)
    elif event.type == Gelly_EventType.MSGEVENT:
      return self.interpretmessage(event,dungeon)
    return False
  #===============================================================================================
  def interpretkeyevent(self, keyevent, dungeon):
    """
    """
    if keyevent.type == Gelly_EventType.KEYUP:
      direc = False
      #===========================================================================================
      # direction keys, directely interpreted as move actions
      #===========================================================================================
      if keyevent.key == SDLKey.SDLK_UP:
         direc = Vector((0,-1))
      elif keyevent.key == SDLKey.SDLK_DOWN:
        direc = Vector((0,1))
      elif keyevent.key == SDLKey.SDLK_RIGHT:
        direc = Vector(( 1,0))
      elif keyevent.key == SDLKey.SDLK_LEFT:
        direc = Vector((-1,0))
      #===========================================================================================
      
      #===========================================================================================
      elif keyevent.key == SDLKey.SDLK_a:
        action = Action( actor  = self.character,
                         atype  = 'attack',
                         target = self.character._target,
                         skill  = self.character.deck[0],
                         stage  = self.character._context,
                         energy = 3 )
        self.character.mind.appendaction( action )
      #===========================================================================================
      elif keyevent.key == SDLKey.SDLK_1:
        #self.character.mind.appendaction( self.makeaction(0) )
        print "gelly UI: button 1 pressed"
      elif keyevent.key == SDLKey.SDLK_2:
        #self.character.mind.appendaction( self.makeaction(1) )
        print "gelly UI: button 2 pressed"
      elif keyevent.key == SDLKey.SDLK_3:
        #self.character.mind.appendaction( self.makeaction(2) )
        print "gelly UI: button 3 pressed"
      elif keyevent.key == SDLKey.SDLK_4:
        #self.character.mind.appendaction( self.makeaction(3) )
        print "gelly UI: button 4 pressed"
      elif keyevent.key == SDLKey.SDLK_5:
        #self.character.mind.appendaction( self.makeaction(4) )
        print "gelly UI: button 5 pressed"
      elif keyevent.key == SDLKey.SDLK_6:
        self.character.mind.appendaction( self.makeaction(5) )
      elif keyevent.key == SDLKey.SDLK_7:
        self.character.mind.appendaction( self.makeaction(6) )
      elif keyevent.key == SDLKey.SDLK_8:
        self.character.mind.appendaction( self.makeaction(7) )
      elif keyevent.key == SDLKey.SDLK_9:
        self.character.mind.appendaction( self.makeaction(8) )
      elif keyevent.key == SDLKey.SDLK_0:
        self.character.mind.appendaction( self.makeaction(9) )
      #===========================================================================================
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
      self.character.mind.appendaction(  Action( atype = 'move',
                                          stage = dungeon,
                                          actor = self.character,
                                          target = direc,
                                          energy = 1 ) )
    return False
  #===============================================================================================
  def interpretmouseevent(self, mevent, dungeon ):
    """
      
    """
    if mevent.type == Gelly_EventType.MOUSEBUTTONUP:
      tile = dungeon.map[mevent.x, mevent.y]
      self._selection.select( tile )
      for item in tile.items:
        if isinstance(item,Character):
          self.character.settarget( item )
          print self.character, "targets", self.character.mind._target
  #===============================================================================================
  def interpretmessage(self, mevent, dungeon ):
      """
      handles messages from any external source
      """
      print "MESSAGE",mevent.target, mevent.action, mevent.message
      try:
        message = ast.literal_eval( mevent.message ) #parse the message component, should yield a dict
        target = getattr(self,mevent.target) #attempt to isolate the target
        action = getattr( target, mevent.action ) #attempt to isolate the action on the target
        action(**message)
        print "testing action"
        print action
        if mevent.action == "setskill":
          return setskillcb()
      except Exception:
        print "something fucked up in interpretmessage"
  #===============================================================================================
  def interpretjsonmessage(self, mevent, dungeon ):
    """
      TODO: json message handling
    """
    return False
  def interpretxmlmessage(self, mevent, dungeon ):
    """
      TODO: xml message handling
    """
    return False
  #===============================================================================================
  def makeaction(self, skillnumb):
    """
    """
#    action = Action( actor  = self._character,
#                     atype  = 'attack',
#                     target = self._character._target,
#                     skill  = self._character.deck[0],
#                     stage  = self._character._context,
#                     energy = 4 )
#    print skillnumb, self._character.deck[skillnumb]._type
#    action = Action( actor  = self._character,
#                     atype  = self._character.deck[skillnumb]._type,
#                     target = self._character._target,
#                     skill  = self._character.deck[skillnumb],
#                     stage  = self._character._context,
#                     energy = 4 )
#    return action
  #===============================================================================================
