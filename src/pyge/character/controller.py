#=================================================================================================
# Controller class
#
#  
#=================================================================================================
 #pygame includes
import sys
sys.path.append("/home/lorin/projects/gelly/objs ")
from actor import Actor

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
    self._model= model = [ (0,0), (0,171), (100,171), (100,0) ]
    self._pos = (-100,-100)
    super( Selection, self ).__init__( model, self._image_file, offset=(0,50))
  #===============================================================================================
  def select(self, tile_actor ):
    """
    """
    self._pos = ( tile_actor._position[0],
                  tile_actor._position[1] )
    self.sel = tile_actor
    print tile_actor
  #===============================================================================================
  def draw(self):
    """
    """
    super(Selection,self).draw(self._pos,"selector")
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
    self.selection = Selection()

  def interpret(self, event, dungeon ):
    """
      interpret the event in terms of the associated character object, returning an action which
      can be used to apply the desired effect to the game state
    """

    if event.type == pygame.KEYUP:
      return self.interpretkeyevent(event,dungeon)
    elif event.type == pygame.MOUSEBUTTONDOWN:
      return self.interpretmouseevent(event,dungeon)
    return False


  def interpretkeyevent(self, keyevent, dungeon):
    """
    """
    if keyevent.type == pygame.KEYUP:
      direc = False
      print keyevent.scancode
      if keyevent.scancode == 114: #directional keys pressed
        print 114
        direc = Vector2(1,0)
      elif keyevent.scancode == 113:
        direc = Vector2(-1,0)
      elif keyevent.scancode == 116:
        direc = Vector2(0,1)
      elif keyevent.scancode == 111:
        direc = Vector2(0,-1)

      elif keyevent.scancode == 38: #a key
        #attacks require a target
        if self.character.target:
          self.character.mind.qaction.append( Action( verb  = Action_Type['attack'],
                                                      actor = self.character,
                                                      target= self.character.target,
                                                      stage = dungeon ) )
      elif keyevent.scancode == 33: #p key
        loc = dungeon.loc(self.character)
        self.character.mind.qaction.append( Action( verb  = Action_Type['grab'],
                                                    stage = dungeon,
                                                    actor = self.character,
                                                    tile  = loc ) )
      elif keyevent.scancode == 32: #o key
        loc = dungeon.loc(self.character)
        self.character.mind.qaction.append( Action( verb  = Action_Type['drop'],
                                            stage = dungeon,
                                            actor = self.character ) )
    if  direc:
      self.character.mind.qaction.append( Action( verb = Action_Type['move'],
                                          stage = dungeon,
                                          actor = self.character,
                                          target = direc) )
    return False
  #===============================================================================================
  def interpretmouseevent(self, mouseevent, dungeon ):
    """
      
    """
    if mouseevent.type == pygame.MOUSEBUTTONDOWN:
      for x in range(dungeon.x_range[0], dungeon.x_range[1]):
        for y in range(dungeon.y_range[0],dungeon.y_range[1]):
          pos = mouseevent.pos
          pos = (pos[0],600-pos[1])                                                              
          if dungeon.map[x,y].collide( pos ):
            self.selection.select( dungeon.map[x,y] )
            #this is messier than I'd like
            #target any character on the tile
            #use filter instead
            for each in dungeon.map[x,y].items:
              if isinstance(each, Character):
                self.character.target = each
                print "TARGETING EVENT: ",self.character," targeted ",each
