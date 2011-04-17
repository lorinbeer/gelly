#=================================================================================================
# Action Class
#  Represents a verb, acted out by a character. 
#  The action class is authored by some agent, such as class Mind instance, or a user
#
#
#=================================================================================================



#=================================================================================================

Action_Type = {'null':0,'move':1,'attack':2, 'defence': 3, 'grab':4,'drop':5}

#=================================================================================================
class Action( object ):
  """
    represents a verb
  """
  actns = ['null', 'move', 'attack', 'defence', 'parry', 'dodge', 'grab', 'drop' ]
  actype = {}
  for i,act in enumerate(actns):
    actype[act] = i
  #actype = {'null':0,'move':1,'attack':2, 'defence': 3, 'grab':4,'drop':5}

  def __init__(self, **kwargs ):
    """
      verb  - what kind of action this object represents, use Action.actype dict to specific
      stage - where the action takes place, usually a dungeonmap object
      actor - in this context, simply the active agent in the formula
      target- the target object of the action
    """
    self.effect = False
    if 'verb' in kwargs.keys():
      if kwargs['verb'] == Action_Type['null']:
        self.verb = Null()
        self._actiontype = Action_Type['null']
        self.args = { }

      if kwargs['verb'] == Action_Type['move']:     #if move action
        self.verb = Move()
        self._actiontype = Action_Type['move']
        self.args = { 'stage' :kwargs['stage'],
                      'actor' :kwargs['actor'],
                      'target':kwargs['target'] }

      elif kwargs['verb'] == Action_Type['attack']: #if attack action
        self.verb = Attack()
        self._actiontype = Action_Type['attack']
        self.args = { 'actor' :kwargs['actor'],
                     # 'attack':kwargs['attack'],
                      'target':kwargs['target'],
                      'stage' : kwargs['stage'] }
        
#        from actor import AnimatedActor
        loc = kwargs['stage'].loc( kwargs['target'] )
        if loc:
          loc = kwargs['stage'].map2screen( loc )
          loc=( loc[0]-50, loc[1]-40 )


        if not loc:
          loc = (0,0)

#        self.effect = AnimatedActor('/home/lorin/projects/ge/art/cut_a' , 20, loc )
#        self.effect = AnimatedActor('/home/lorin/projects/ge/art/cut_a', 20, kwargs['target']._position )
        
      elif kwargs['verb'] == Action_Type['grab']:
        self.verb = Grab()
        self._actiontype = Action_Type['grab']
        self.args = { 'stage' :kwargs['stage'],
                      'actor' :kwargs['actor'] }
                    #  'target':kwargs['target'],
                    #  'tile'  :kwargs['tile'] }
      elif kwargs['verb'] == Action_Type['drop']:
        self.verb = Drop()
        self._actiontype = Action_Type['drop']
        self.args = { 'stage' :kwargs['stage'],
                      'actor':kwargs['actor'] }
    else:
      raise some_exception
    
    

  
  #for now, just assumes we are performing a move action
  def act(self):
    """
    """
    
    self.verb(self.args)
    return self.effect


class ActionFactory(object):
  """
  """
  action_types = {'move': 0, 'attack': 1  }

  def make_action(self,action_type):
    """
    """
    new_action = Action()
    return new_action




class Move(object):
  """
  """
  def __call__(self, args):
    """
    """
    args['stage'].move_character( args['actor'], args['target'])        

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
    
