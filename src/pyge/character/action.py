#=================================================================================================
# Action Class
#    The Action class is authored by some agent, and encapsulates all the information neccesary
#    to perform the desired action
#
#=================================================================================================
#=================================================================================================

#=================================================================================================
#=================================================================================================
class Action( object ):
  """
   Represents a verb
   
    The action class is authored by some agent, and encapsulates all the information neccesary
    to perform the desired action
  """
  _actions = { 'null'   : [],
            'move'   : ['actor','target','stage','energy'],  #move actor to target on stage
            'attack' : ['actor','target','skill','stage','energy'], #actor attacks with skill on stage
            'defence': ['actor','skill','energy'], #actor defends with skill at energy
#           'parry'  : ['actor','skill','energy'], 
#           'dodge'  : ['actor','skill','energy'],
            'grab'   : ['actor','target','tile','stage'],
            'drop'   : ['actor','stage'] }
  #===============================================================================================
  def __init__(self, **kwargs ):
    """
      verb  - what kind of action this object represents, use Action.actype dict to specific
      stage - where the action takes place, usually a dungeonmap object
      actor - in this context, simply the active agent in the formula
      target- the target object of the action
    """
    self.effect = False
    if 'atype' not in kwargs.keys(): 
      #default initialization to 'null' action
      self.__initnull__()
    else:
      try:
        #passed a valid type
        self.type = kwargs['atype']
        for arg in self._actions[ self.type ]:
          setattr( self, arg, kwargs[arg] )
        self._effect = kwargs.get( 'effect', None )
      except KeyError:
        #TODO redirect to error log
        print "Missing a necessary argument for Action, or Invalid Action type"
        print kwargs
  #===============================================================================================
  def __initnull__(self):
    """
    default initialization to 'null' object
    """
    self.type = 'null'
    self.energy = 0
    self.args = { }  
  #===============================================================================================
  def skilltype(self):
    """
      utility function for accessing an action's skilltype
    """
    return self.skill.skilltype()
  #===============================================================================================
  def targetnumber(self):
    return self.skill.targetnumber( self.energy )
  def match(self, targetnumber):
    return self.skill.match( targetnumber )
  #===============================================================================================
  def setenergy(self, **kwargs ):
    """
      given an energy value, attempt to set this skill's energy value to match
      given a target number, attempts to set this skill's energy to match the target numebr
      this can fail if:
        the energy value exceeds the skills max energy
        the character does not have enough energy
    """
    if self.type == 'null':
      return False
    if "targetnumber" in kwargs:
      energy = self.tntoenergy( kwargs["targetnumber"] )
    else:
      energy = kwargs["energy"]
    if self.actor.hand() >= energy and self.skill.maxenergy <= energy:
      self.energy = energy
    return True
    

#=================================================================================================


#=================================================================================================

class Move(object):
  """
  """
  def __call__(self, args):
    """
    """


class Attack(object):

  from math import pow
  """
  """
  def __call__(self,args):
    """
      resolves combat based on a physical attack

      calculate the terminal velocity of the attack (the speed at the point of the impact)
      calculate the kinetic energy of the weapon given the speed

      actor
      ability:
      target:  
    """
    if not args['actor'].target.alive: return False
    print 'attack %(target)s' % { 'target': args['actor'].target }
    from dungeon.dungeonmaster import DungeonMaster
    dm = DungeonMaster( args['stage'] )

    attack_time = 0.5 #for now, all attacks are heavy
    
      #calculate terminal velocity (speed) weapon travels from rest
    weapon_speed   = args['actor'].strength * ( 1 / args['actor'].weapon.mass  ) * attack_time
      #calculate distance weapon travels given
    weapon_dist    = (1.0/ 2.0 ) * weapon_speed * attack_time
      #calculate kinetic energy of weapon
    weapon_kenergy = (1.0/2.0) * pow(weapon_speed,2) * args['actor'].weapon.mass 

    print 'Weapon Speed: %(ws)s' % {'ws':weapon_speed}
    print 'Weapon Distance: %(wd)s' % { 'wd':weapon_dist}
    print 'Weapon Kinetic Energy: %(ke)s' % {'ke': weapon_kenergy}

      #calculate 
    target_dist=(1.0/2.0)*args['target'].agility*(1.0/args['target']._mass)*attack_time*attack_time
    tweapon_speed=args['target'].strength*( 1 / args['actor'].weapon.mass  ) * attack_time
    print 'Target Speed: %(ts)s' % {'ts': target_dist}
    
    #=============================================================================================
      #hit automatically, cause a wound
    args['target'].health -= weapon_kenergy
    if args['target'].health <= 0:
      print 'target death'
    print 'hit! target health: %(th)s' % {'th': args['target'].health }
    dm.foo( args['target'] )
    #=============================================================================================
  

class Grab(object):
  """
  """
  def __call__(self,args):
    """
      picks up the first non-character gitem sharing the tile with the actor and places it in
      the actor's inventory   
      stage: the map the actor is currently in
      actor: the character performing the action
    """
    from character import Character
    stage = args['stage']
    actor = args['actor']
    pos = stage.loc( actor ) #get the location of the actor
    tile = stage.map[pos.x,pos.y]
    for each in tile.items:
      if each != actor and not isinstance(each,Character):
        actor.inventory.append(each)
        stage.remove(each)
    

class Drop(object):
  """
  """
  def __call__(self,args):
    """
    """
    from character import Character
    stage = args['stage']
    actor = args['actor']
    pos = stage.loc( actor ) #get the location of the actor
    stage.place( actor.inventory.pop(),
                 (pos.x,pos.y))

class Null(object):
  """
    "THE GOGGLES DO NOTHING"
  """
  def __call__(self,args):
    """
    """
    
