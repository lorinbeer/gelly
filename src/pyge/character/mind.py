#=================================================================================================
# Mind Class
#  AI class for character objects
#  
# Lorin Beer
# ldabeer@gmail.com
# 
#beturby algorithm pathfinding
#=================================================================================================
#=================================================================================================
from dungeon.dungeon import DungeonMap
from action import Action
from skill import Skill, SkillFactory
from util.vector import Vector
from math import sqrt,fabs
import random
#=================================================================================================
#=================================================================================================
class Mind(object):
  """
    AI Class for character objects
  """
  def __init__(self, **kwargs ):
    """
      ego - reference to the 'self' that this Mind is attached to
      factionid - integer representing the faction this mind is allied with. Default is 0, the
                  neutral faction
    """
    try:
      self._ego       = kwargs['ego']
      self._factionid = kwargs.get('factionid', 0)
    except KeyError:
      print "Character Mind Init Error: missing neccesary argument in initialization" 

    self._actionqueue = list()
    self._target = None
    
    sf = SkillFactory()
    parry = sf.makeskill('parry',1)
    dodge = sf.makeskill('dodge',1)
 
    self._reactions = [None,None,None]
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
    #if this character is dead, append generate a null action and return
    if not self._ego._alive:
      self.qaction.append( Action() )
      return

    #scan the dungeon for other character objects
    for char in dungeon.characters.items():
      if self.friendorfoe(char[1]) < 0:
        target = char[1]
        targetloc = Vector( (char[0][0], char[0][1]) )
      elif char[1].name == self._ego.name:
        me = char[1]
        myloc = Vector( (char[0][0], char[0][1]) )

    dirVec = targetloc - myloc    #calculate a vector to the target
    print 'dirVec', dirVec
###distance check####
#check abilities against current distance in order to determine what action to take
#    print "direction vec mag: %(magnitude)s" %{'magnitude': dirVec.magnitude() }
#    print myloc

    if dirVec.magnitude() < 2:
      action = Action()
    else:
      dirVec.normalized() #normalize and round to get a unit vector towards the target
      dirVec.ctint()

      action = Action( atype   = 'move',
                       actor  = self._ego,
                       stage  = dungeon,
                       target = dirVec,
                       energy = 1 )
      print "MIND ACTION", action
    self._actionqueue.append( action )
  #===============================================================================================
  def targetalive(self):
    """
      utility function for checking the status of this mind's target
      returns True if the target is alive, false otherwise
    """
    if self._target:
      if self._target._alive: return True
    return False
#=================================================================================================
  def friendorfoe( self, target=None ):
    """
      Attempt to identify a target as an ally or enemy
      INPUT:
        target - the target to test, if the target does not have a fofid, then the result is
                 always 0 (neutral)
      OUTPUT: an integer representing the target's status
              - > 1 : target is an ally
              - < 1 : target is an enemy
              -  0  : target is neutral 
    """
    if not target: target = self._target #if no target is supplied, use the current target
    if not target: return  #if there is still no target, return
    if self._factionid==0 or target.mind._factionid==0:
      return 0
    elif self._factionid != target.mind._factionid:
      return -1
    return 1
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
