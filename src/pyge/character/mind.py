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

from action import Action, Action_Type

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
    self.ego = ego
    self.qaction = list()
    from skill import Skill
    defence = Skill(name= 'parry',
                    level= 1,
                    threshold= 2,
                    stype = Action.actype['parry'],
                    effect= Action.actype['defence'])
    defence.setenergy(4)
    self._reaction = [defence,defence,None]
    self._disabled = False
  #==============================================================================================
  def getaction(self):
    """
      returns an action for this character to perform
    """
    if len(self.qaction):return self.qaction.pop(0)
    elif self._disabled: return False
    else:
      self.plan( self.ego._context )
      return self.qaction.pop(0)
  #==============================================================================================
  def getreaction(self):
    """
      returns a defense action for this character to perform
    """
    return self._reaction[ random.randint(0,2) ]
  #==============================================================================================
  def plan(self, dungeon):
    """
      given the environment the ego is currently in, author an Action object



      """
    #identify a target and ego on the map
#    print 'mind of %(name)s' %{'name': self.ego.name }


    if not self.ego._alive:  
      action = False#Action( verb = Action.actions['null'] )
      self.qaction.append( action )
      return

    for each in dungeon.characters.items():
      if each[1].name != self.ego.name:
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
      action = Action( verb = Action_Type['null'] )
    else:
      dirVec = dirVec.normalized() #normalize and round to get a unit vector towards the target
      dirVec.x = round(dirVec.x)   
      dirVec.y = round(dirVec.y)

      action = Action( verb   = Action_Type['move'],
                     actor  = self.ego,
                     stage  = dungeon,
                     target = dirVec )
    self.qaction.append( action )
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


#find a target
#calculate a direction vector towards the target
#calculate the tile which corresponds to the direction vector
#move to that square
#


#pick a target
#calculate distance to target
