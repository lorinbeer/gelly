#=================================================================================================
# Dungeon Master Class
#
#
#=================================================================================================

#from dungeon import Dungeon

#from character import Character

from character.action import Action, Action_Type

from battlemaster import BattleMaster

#=================================================================================================
#TODO#
#1. list of characters should be a priority queue sorted in turn order
#=================================================================================================
class DungeonMaster(object):
  """
  """
  def __init__(self,dungeon):
    """
    """
    print "Initializing DM"

    self.dungeon = dungeon
    self.battlemaster = BattleMaster( )
    #=============================================================================================
    self._characters = list( )
    for each in dungeon.characters.values( ):
      self._characters.append( each )
    self._current = 0
    #=============================================================================================
    #internal state flags
    self._hold = False #indicates 'paused' state of DM
    #=============================================================================================
  #===============================================================================================
  def resolve_action( self, action ):
    """
      
      actor - the acting object, whatever is attempting the action 
      action - the action to be performed
      target - the target of the action
    """
    print "Dungeon Master: Resolve Action"
    if action._actiontype == Action_Type['attack']:
      self.battlemaster.resolve_combat( action.args['actor'], 
                                        None, 
                                        action.args['target'],
                                        action.args['stage']  )
      return action.effect
    else:
      return action.act( )
  #===============================================================================================
  def resume( self ):
    """
      
    """
    self._hold = False
  #===============================================================================================
  def turn( self ):
    """
      calculate a full game turn
    """
    #ask each character for an action
    effects = list()
#    print self._characters
    while not self._hold:
      char = self._characters[self._current]
      char.update() #ready the character for this turn
      action = char.mind.getaction() #request an action from the current character
      if action: #npc's will always return an action, might have to wait on pc's
        effects.append( self.resolve_action( action ) )
      else: #pc's will return false if no action is in the queue
        return effects#in this case, we return, waiting for character to perform an action
      self._current += 1 #move to the next character
      if self._current >= len(self._characters): #circular increment
        self._current = 0 #loop back to the first
        break
    print self._current
    return effects

  #===============================================================================================
  def update( self ):
    """
      update the internal state

      handles checks for dead characters/objects
    """
    for character in self._characters:
      print character, character._health
      if character._health <= 0:
        character._alive = False
    self.prune()
  #===============================================================================================
  def prune( self ):
    """
      Remove (prune) all dead objects from the internal lists
    """
    prune = [character for character in self._characters if not character._alive]
    self._characters = [character for character in self._characters if character not in prune]
    for character in prune:
      self.dungeon.remove( character )
#=================================================================================================
