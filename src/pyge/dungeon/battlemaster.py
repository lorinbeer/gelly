#=================================================================================================
#  BattleMaster
#    primary implementation of the combat system
#    contains functions for calculating a full combat action resolution, as well as functions
#    for calculating necessary intermediate value
#  author - Lorin Beer
#  emal   - ldabeer@sfu.ca
#=================================================================================================
#TODO
# implement safeguards for attacking non character objects
# implement handling of no weapon equiped
# handle not being able to dodge, parry, block gracefully ie cannot parry without a weapon
# add ability to carry over velocity from one attack to another, ie V_i support
# migrate physics calculations to a proper physics subsystem
# more complex parry conditions
#
#
#NOTES
# the combat dictionary may seem cumbersome, with the many awkward abbreviated keys
# however, it offers a simple way of applying modifers to any relevant value without having to
# write any additional code: the modifier is simply passed as a tuple with a value and a key to
# modify
#
#=================================================================================================

import math
import random # ugh.

#=================================================================================================

from character.skill import Skill
from character.action import Action
from physics import *

#=================================================================================================
class BattleMaster(object):
  """
    Primary implementation of the combat system.
    Contains functions for resolving combat actions, and calculating intermediate values.
  """
  def __init__(self):
    """
      initialize internal BattleMaster settings
    """
    self._str_attack_force_mult = 20.0 #20.0 kg*m/s^2 per str point, used to calculate wpn accel
    self._str_impact_force_mult = 50.0 #50.0 kg*m/s^2 per str point, used to calculate impact F
#    self._agi_force_mult = 0.0 #0.0 kg*m/s^2 per agi point, used to calc movement speed
#
  #===============================================================================================
  #===============================================================================================
  #
  # Private Functions
  #
  #===============================================================================================
  #===============================================================================================
  def __impactforce__(self, strength ):
    """
      returns the force behind a weapon at the moment of impact based on the strength attribute

      this is distinct from __attackforce__, which calculates the force used to accel a weapon

      this function essentially a characters strength attribute to Force in kg*m/s^2, for the
      purposes of calculating the force behind the weapon at the moment of impact
      which can then be given to the physics system for calculating further values
    """
    return self._str_impact_force_mult * float(strength)
  #===============================================================================================
  def __attackforce__(self, strength ):
    """
      returns the force a character is able to exert on a weapon while attacking

      this is distinct from __impactforce__, which calculates the force of a blow

      this function translates a characters strength attribute to Force in kg*m/s^2,
      which can then be given to the physics system for calculating further values
    """
    return self._str_attack_force_mult * float(strength)
  #===============================================================================================
  #===============================================================================================
  #
  # Public Interface
  #
  #===============================================================================================
  #===============================================================================================
  def resolve_combat(self, attacker, attack, defender, dungeon):
    """

    attacker - the character performing the attack
    skill    - the skill the attacker is using
    attack   - the attack being performed
    defender - the target of the attack
    """
    print "Battle Master: Resolve Combat"
    print "Attacker Energy: %s " % (attacker._energy)
    print "Defender Energy: %s " % (defender._energy)
      ###TODO###
        #for now, all attacks are assumed to be slash attacks, and all defense are parries
    attack = Skill( name= 'slash',
                    level= 3,
                    threshold= 2,
                    damagetype= 'cut',
                    effect= Action.actype['attack'] )
    attack.setenergy(4)
      ###/TODO###
    cd = {}


    #Check for relevant status effects which might effect the flow of combat
    # these should be moved to a config file
    # config file should contain classes of status effects
 


#      if False:
#        for stat,mult in ability.multiplier.items():
#          if stat in combatdict:
#            combatdict[stat] *= mult        
#        for stat,summand in ability.summand.items():
#          if stat in combatdict:
#            combatdict[stat] += summand 


    #Defense
    defresult = self.resolve_defense( attacker, attack, defender, cd )
    attacker.use( attack._energy )
    defender.use( defresult['cost'] )
    defender._wounds.append(defresult['wound'] )
    print "Defense Result: ", defresult

  #=============================================================================================
  def resolve_defense(self, attacker, attack, defender, cd):
    """
      calculate the result of a defender's defense (re)action to an attack
      INPUT:
           -attacker: attacking character 
           -defender: defending character
           -attack: the attack object the attacker is using
           -cd:
      OUTPUT: dictionary with the following keys
               reaction: the reaction 'chosen' by the defender (parry, dodge or block)
               success: True/False if the reaction was successful/unsuccessful
                        a parry or dodge is successful if the attack is evaded, a block is 
                        successful if the attack lands on armour, even if a wound is incurred
               cost: the energy cost to the defender given the chosen action 
               wound: the wound (if any) caused by the attack
    """


    defencecost = 0
    success = False
    wound = None
    
    defence = defender.mind.getreaction() #retrieve defense action from defender
    
    #1. handle attemts to attack or parry
    if defence:
      if defence.skilltype() == Action.actype['parry']: # and self.can_parry( defender, attack ):
        (success, defencecost) = self.parry( attack, defence) #resolve parry
      elif defence.skilltype() == Action.actype['dodge']:
        (success, defencecost) = self.dodge() #resolve dodge
    #2. handle a possibly successful defence action
    #   if use returns false, it means the user had insuficient energy in hand for the action
    if success and not defender.use( defencecost, True ):
      print "DEFENCE FAIL"
      success = False

    #3. handle unsuccessful defence by resolving armour penetration and any resulting  wounds
    if not success: #resolve_block, can always block, just like you can always get hit it the face
      if False: #self.armour_hit( cd['dcov']  ):
        self.armour_penetration( defender , attack )
      print "FUCKED IN THE FACE!"
      wound = self.wound_resolution( defender=defender , attack=attack )
        #self.wound = wound_resolution( character , 

    result = { 'reaction': defence,
               'success' : success,
               'cost'    : defencecost,
               'wound'   : wound }

    return result
  #===============================================================================================
 
  #===============================================================================================
  def can_parry(self, character, attack ):
    """
      Determine if character is capable of attempting a parry against attack.

      A character can attempt a parry if:
        one of his equiped weapons is capable of parrying
        he has no relevant status effects or buffs that would prevent parrying
        the attack can be parried
      INPUT:
           -character: the character object to test
           -attack: the attack character is attempting to parry
      OUTPUT: True if the character is capable of performing a parry, false otherwise
    """
    #TODO: -add check against character buffs/debuffs
    #      -add check agaist attack (some attacks are unpariable)
    #check each weapon slot on the character, if one is able to parry, then return true
    for slot in character._equipment._weapon_slots:
#      print slot
      if character._equipment[slot]._parry:
        return True
    return False
  #===============================================================================================
  def parry( self, attack, defence ):
    """
      Determine the result of an attack vs defense skill test

      OUTPUT: tuple containing pass/fail result of parry, and cost
    """
    #can attack be parried?
    atkTN = attack.targetnumber()
    if atkTN <= defence.targetnumber(): #defence moves' TN will is max that skill is capable of
      return True, atkTN #defence is successful, return the cost to the defender 
    return False, atkTN  #defence is unsuccessful, but the defender still incurs a cost
  #===============================================================================================
  def can_dodge( self, character, attack ):
    """
      Determine if character is capable of attempting a dodge against attack.

      A character can attempt a dodge if:
        he has no relevant status effects or buffs that would prevent dodging
        the attack can be dodged
      INPUT:
           -character: the character object to test
           -attack: the attack character is attempting to dodge
      OUTPUT: True if the character is capable of performing a dodge, false otherwise
    """#can always block, just like you can always get hit it the face  
    #TODO: -add check against character buffs/debuffs
    #      -add check agaist attack (some attacks are undodgeable)
    #check each weapon slot on the character, if one is able to parry, then return true
    return True
  #===============================================================================================
  def dodge( self ): 
    """
      current - a comparison of the attackers weapon speed to the defenders movement speed
    """
#    physics = Physics()
#    awVf = physics.velAT( cd['awpna'], atk_time ) #final velocity of attacker's weapon
#    if cd['dspe'] >= awVf:
#      return True
    return (True, 100)
  #===============================================================================================
  def armour_hit( self , dcoverage ):
    """
      determine whether an attack hits armour, or an exposed part of the wearer

      currently implemented as a naive dice roll which does not take into account attacker skill
      or targeting specific body parts
      INPUT:
            dcoverage: the defender's coverage stat
      OUTPUT:
            True : hit falls on armour
            None: hit falls on unarmoured
    """
    roll = random.randint(1,100) #roll a d100
    if roll > dcoverage: return True
  #===============================================================================================
  def armour_penetration( self, character, attack ):
    """
    """
    return False
  
  #===============================================================================================
  def wound_resolution ( self , **kwargs  ):
    """
      given a context (wound table, location, strength of hit, type of hit and weapon), returns the wound inflicted.

      This Function just returns the wound that would be inflicted given the context, it does not
      resolve the effect of the wound on a character instance
      INPUT:
        table   : wound lookup table
        location: where the hit hit
        damagetype : how the hit hit (slashing, bashing, piercing)
        energy  : effective strength of the hit
        weapon  : whatever's doing the hitting 
      OUTPUT:
        returns a wound object
    """
    return True
  #===============================================================================================

#=================================================================================================
