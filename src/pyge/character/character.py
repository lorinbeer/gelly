#=================================================================================================
# Character Class
#
#
#
#=================================================================================================
#TODO
# equipment, character, and battlesystem support for multiple weapon hands
#=================================================================================================
import sys
sys.path.append("/home/lorin/projects/gelly/obs")
#=================================================================================================
from actor import Actor, Vertel
from mind  import Mind
from energy import Energy
from skillbook import SkillBook
from action import Action
from inventory import Inventory
from buffable import Buffable
#=================================================================================================
class Equipment( dict ):
  """
    #head #neck  #shoulders #rl upper arm #rl elbow #rl lower arm #rl hand #chest #belly #back
    #groin #rl upper leg #rl knee #rl lower leg #rl foot #mainhand #offhand #
  """
  def __init__(self):
    """     
    """
    #
    super( Equipment, self).__init__()

    #migrate to settings db
    self._equipment_slots = ("head", "shoulders", "torso", "hands", "legs", "feet", "mainhand")
    self._weapon_slots = ("rhand", "lhand")

    #initialize each equipment slot to None
    for slot in self._equipment_slots:
      self[slot] = None
    for slot in self._weapon_slots:
      self[slot] = None

    self.coverage = 0.0 #coverage stat offered by currently equiped item
  #===============================================================================================
  def equip(self, item):
    """
        equip the given item, returning the item in that slot
        if no item equiped, returns None
        if item is not of correct type, raises TypeError
    """
    try:
      if item._slot in self:
        current = self[ item._slot ]
        self[ item._slot ] = item
        #self._coverage += (item._coverage - current._coverage)
        return current
      else: return False
    except AttributeError:
      raise TypeError
  #===============================================================================================
  def drop(self, item_slot):
    """
    """
    try:
      current = self[item_slot]
      self[item_slot] = None
      if current:
        self.coverage -= current.coverage
      return current
    except AttributeError:
      raise TypeError
#=================================================================================================
class Stat( object ):
  """
  """
  def __init__(self, stat_type):
    """
    """
    self._behave = stat_type
#=================================================================================================
#=================================================================================================

#=================================================================================================
#=================================================================================================
class Deck( dict ):
  """
    An active skill list, holding those skills which a character can activate in combat
    
    A Deck object is not a generalized container, as is designed to only contain objects which
    implement a Skill type interface
  """
  #===============================================================================================
  def __init__(self, **kwargs):
    """
      INPUT:
        maxsize    (int)  - maximum number of skills allowed in the deck at any one time
        skillslots (list) - the slots to initialize the deck with  the skills to initialize the 
                            deck with, if any only copies up to maxsize skills from this list
    """
    super(Deck,self).__init__()
    self._maxsize = kwargs.get('maxsize',6)
    self.slots = {}
    self.skills = self
    slots = kwargs.get('slots', [])
    skills = kwargs.get('skills',[])
    for i in range(0,self._maxsize):
      key = 'SLOT_%i'%(i)
      if i < len(slots):  self.slots[key] = slots[i]
      else: self.slots[key] = 'default'
      if i < len(skills): self[key] = skills[i]
      else: self[key] = None
  #===============================================================================================
  def getslot(self,key):
    """
    """
    return self.slots[key]
  #===============================================================================================
  def getskill(self,key):
    """
    """
    return self[key]
  #===============================================================================================
  def setskill(self,**kwargs):
    """
    """
    try:
      print kwargs
      print  'KSILL<',kwargs['skill']
      self[kwargs['slot']] = kwargs['skill']
    except KeyError:
      print "KeyError: missing argument"
  #===============================================================================================
  def setslot(self,**kwargs):
    """
    """
    try:
      self.slots[kwargs['slot']] = kwargs['type']
    except KeyError:
      print "KeyError: missing argument"
    print self.slots
    print self.skills
  #===============================================================================================
#=================================================================================================
#=================================================================================================

#=================================================================================================
#=================================================================================================
class Character( Actor ):
  """
  """
  #===============================================================================================
  def __init__(self,name,imagefile,context,skills=[],factionid=0):
    """
    """
    model = [ (0,0), (0,181), (100,181), (100,0) ]
    bounding_rect = [ (0,0), (0,181), (100,181), (100,0) ]
    #super( Character, self ).__init__( model, imagefile, offset=(0,50) )
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
    super( Character, self ).__init__( imagefile, _model, _bound )
    #self.name = kwargs.get('name',"Unnamed")
    self.name = name
    self.mind = Mind( ego=self, factionid=factionid ) 

    self._controller = None

    self._context = context

    self._target = None

    #body stats
    self.strength  =  10  #strength of character, in kg*m*s^-2
    self.agility   =  20  #agility of character,  in kg*m*s^-2
    self.endurance =  10  #endurance: MAX Energy Reserves, in 
                          #endurance 
                          #endurance: MAX energy output in watts in kg*m^2*s^-3
    self._reach = 1.0     #arm length
    self._mass   = 50   #mass of character, in kg
    self.health = 100  #

    self.energy = Energy()

    self._alive  = True #alive bit, used to drop a character object references

    #skills
    self.skillbook  = SkillBook(skills=skills) 
    self.deck       = Deck(maxsize=4, slots=['default']*6 )

    #equipment
    self._equipment = Equipment()     #equipment is currently held by the character
    self.inventory = Inventory(40.0) #items in storage
    self.weapon = None

    #modifiers
    self.buff = Buffable(self) #allows the character to be buffed (stat and status effects)
    self.status_effects = []
    self._wounds = []
  #===============================================================================================
  # Helper functions which link related members of a Character object, such as the skll book and
  # skill deck
  #===============================================================================================
  def setslot(self,**kwargs):
    """
      helper function, sets deck slot type
    """
    self.deck.setslot(**kwargs)
  def setskill(self,**kwargs):
    """
      helper function, sets deck slot with skill from skillbook
    """
    self.deck.setskill(slot=kwargs['slot'],skill=self.skillbook[kwargs['skill']])
  def queueskill(self,**kwargs):
    """
      helper function, queues a skill as the next action from the deck
      
    """
    print "Character queue skill"
    try:
      skill = self.deck[kwargs['slot']]
      if skill:
        self.mind.appendaction( Action( actor  = self,
                                        atype  = skill.type,
                                        target = self.mind._target,
                                        skill  = skill,
                                        stage  = self._context,
                                        energy = 3 ) )
        
      else:
        print "No Skill set for deck slot:", kwargs['slot']
    except KeyError:
      print "KeyError in Character:",self.name," queueskill"
      print "  Either 'slot':'val' not present in arguments, or 'slot' not in deck"
      print "  Keys in deck", self.deck.keys()
      print "  kwargs:", kwargs
  #===============================================================================================
  def reach(self):
    """
      return the characters effective reach, 
      taking into account
       - base reach
       - weapon reach
    """
    return ( self._reach + self._equipment["rhand"]._reach )
  #===============================================================================================
  def __str__(self):
    """
    """
    return 'Character: %(name)s' %{'name':self.name}
  #===============================================================================================
  def recharge(self,step=1):
    """
      recharge is the turn update function, called recharge to avoid ambiguity with the animated
      actor's update function. Recharge is called at the beginning of a character's turn.
    """
    self.energy.rechargehand() #draw a new hand of energy from the pool
    #todo decrement cooldown on abilities by 1
  #===============================================================================================
  def use(self, energy, attempt=False):
    """
      remove the specified amount of energy from this characters' hand
    """
    return self.energy.subhand(energy,attempt)
  #===============================================================================================
  def hand(self):
    """return the current energy left in this characters' hand"""
    return self.energy._hand
  #===============================================================================================
  def pool(self):
    """return the current energy left in this characters' pool"""
    return self._energy_pool
  #===============================================================================================
  def iscapable(self, action):
    """
      return True if this character is capable of performing the action, False otherwise

      whether a character is capable of performing a given action or not is dependent on the
      energy cost of the action, and any relevant status effects on the character
    """
    if self.energy._hand >= action.getenergy():
      return True
  #===============================================================================================
  def update(self, step=1):
    """
    """
    #call super class update
    self.recharge(step)
    self.health -= len(self._wounds)*25
    #mind.plan
    return self.health
  #===============================================================================================
  def settarget(self, item ):
    """
    """
    self._target = item
    self.mind._target = item
  def gettarget(self):
    """
    """
    return self._target
  #===============================================================================================
  def listen(self):
    """
      TODO: Make character an event listener
      TODO: this should be an event handler
            currently just updates wound and energy
    """
    #call super class update
    self.recharge(1)
    self.health -= len(self._wounds)*25
    #mind.plan
    if not self.mind.targetalive(): self.mind._target = None
    return self.health
  #===============================================================================================
#=================================================================================================
