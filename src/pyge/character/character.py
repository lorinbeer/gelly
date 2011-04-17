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
from actor import Actor
from mind  import Mind
from energy import Energy
from skillbook import SkillBook
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
class Character( Actor ):
  """
    
  """
  #===============================================================================================
  def __init__(self,name,imagefile,context,skills=[]):
    """
      
    """
    model = [ (0,0), (0,181), (100,181), (100,0) ]
    bounding_rect = [ (0,0), (0,181), (100,181), (100,0) ]
    #super( Character, self ).__init__( model, imagefile, offset=(0,50) )
    super( Character, self ).__init__( imagefile )
    #self.name = kwargs.get('name',"Unnamed")
    self.name = name
    self.mind = Mind( self ) 

    self._controller = None

    self._context = context

    self.target = None


    

    #body stats
    self.strength  =  10  #strength of character, in kg*m*s^-2
    self.agility   =  20  #agility of character,  in kg*m*s^-2
    self.endurance =  10  #endurance: MAX Energy Reserves, in 
                          #endurance 
                          #endurance: MAX energy output in watts in kg*m^2*s^-3
    self._reach = 1.0     #arm length
    self._mass   = 50   #mass of character, in kg
    self._health = 100  #

    self._energy = Energy()

    self._alive  = True #alive bit, used to drop a character object references

    #skills
    self._skillbook  = SkillBook(skills=skills) 
    self._skilldeck = None

    #equipment
    self._equipment = Equipment()     #equipment is currently held by the character
    self.inventory = Inventory(40.0) #items in storage
    self.weapon = None

    #modifiers
    self.buff = Buffable(self) #allows the character to be buffed (stat and status effects)
    self.status_effects = []
    self._wounds = []
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
    self._energy.rechargehand() #draw a new hand of energy from the pool
    #todo decrement cooldown on abilities by 1
  #===============================================================================================
  def use(self, energy, attempt=False):
    """
      remove the specified amount of energy from this characters' hand
    """
    return self._energy.subhand(energy,attempt)
  #===============================================================================================
  def hand(self):
    """return the current energy left in this characters' hand"""
    return self._energy._hand
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
    if self._energy._hand >= action.getenergy():
      return True
  #===============================================================================================
  def update(self, step=1):
    """
    """
    #call super class update
    self.recharge(step)
    self._health -= len(self._wounds)*25
    return self._health
  #===============================================================================================
#=================================================================================================
