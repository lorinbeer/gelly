#=================================================================================================
# Mind Class
#  AI class for character objects
#  
# Lorin Beer
# ldabeer@gmail.com
# 
#beturby algorithm pathfinding
#=================================================================================================

import random

from dungeon.dungeon import DungeonMap

from action import Action

from skill import Skill, SkillFactory

from math import sqrt,fabs

from other.euclid import Vector2

#=================================================================================================

#=================================================================================================

class Mind(object):
  """
    AI Class for character objects
    ego : the context for the mind
    actions : 
    reactions :
  """
  def __init__(self, ego):
    """
      ego - reference to the 'self' that this Mind is attached to
    """
    self._ego = ego
    self._actionqueue = list()
    self._target = None
    
    
    sf = SkillFactory()
    parry = sf.makeskill('parry')
    dodge = sf.makeskill('dodge')
 
    self._fofid = 1;
    self._reactions = [parry,dodge,None]
    self._disabled = False
  #==============================================================================================
  def getaction(self):
    """
      returns the action(s) this character wishes to perform this turn
    """
    if len(self._actionqueue):return self._actionqueue.pop(0)
    elif self._disabled: return False
    else:
      self.plan( self._ego._context )
      return self._actionqueue.pop(0)
  #==============================================================================================
  def appendaction( self, action ):
    """
    """
    self._actionqueue.append(action)
  #==============================================================================================
  def getreaction(self, **kwargs):
    """
      returns a defense action for this character to perform
    """
    if 'attack' in kwargs:
      print "we should analyse the attack"
    reaction = self._reactions[ random.randint(0,2) ]
    if reaction:
      return Action( atype = "defence",
                     actor = self._ego,
                     skill = reaction,          
                     energy = 0 )
    return Action() #if no reaction, return a null action 
  #==============================================================================================
  def plan(self, dungeon):
    """
      given the environment the ego is currently in, author an Action object
    """

    if not self._ego._alive:  
      action = False#Action( verb = Action.actions['null'] )
      self.qaction.append( action )
      return

    for each in dungeon.characters.items():
      if each[1].name != self._ego.name:
        target = each[1]
        targetloc = Vector2( each[0][0], each[0][1] )
      else:
        me = each[1]
        myloc = Vector2( each[0][0], each[0][1] )
  # print "target %(targ)s at %(loc)s" %{'targ':target.name, 'loc': targetloc }
    
   # print 'right here' x
   # print dungeon.item_loc( self.ego )

    dirVec = targetloc - myloc    #calculate a vector to the target

###distance check####
#check abilities against current distance in order to determine what action to take
#    print "direction vec mag: %(magnitude)s" %{'magnitude': dirVec.magnitude() }
#    print myloc

    if dirVec.magnitude() < 4:
      action = Action()
    else:
      dirVec = dirVec.normalized() #normalize and round to get a unit vector towards the target
      dirVec.x = round(dirVec.x)   
      dirVec.y = round(dirVec.y)


      action = Action( atype   = 'move',
                       actor  = self._ego,
                       stage  = dungeon,
                       target = dirVec,
                       energy = 1 )
      print "MIND ACTION", action
    self._actionqueue.append( action )
#=================================================================================================
  def FriendOrFoe( self, target ):
    """
      Attempt to identify a character as an ally or target
    """
    if self._fofid != target.mind._fofid:
      return True;
    return False
#=================================================================================================
  def rand_move( currentposition ):
    """
      this function sucks
    """
    randdir = []
    randdir.append( currentposition[0] + random.randint(-1,1) )
    raddir.append( currentposition[1] + random.randint(-1,1) )
    for i in range(0,2):
      if randdir[i] < 0:
        randdir[i] = 0
      elif randdir[i] > 9:
        randdir[i] = 9
    return randdir
#=================================================================================================
#=================================================================================================
# MIND Algorithms
#
#
#  MOVE
#
#
#  FOF - subsystem to id allies and targets
#    first pass
#    - id code
#    - a character object broadcasts
#
#    - matching ID codes
#      - a child inherits the id code of its parents
#      - a generator can assign id codes arbitrarily
#  
#=================================================================================================
#=================================================================================================
