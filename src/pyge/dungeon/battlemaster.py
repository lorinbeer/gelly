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
  def resolve_combat( self, attack ):
    """
    resolve a combat action
      attack - any object with a properly implemented Action interface
    """
    print "Battle Master: Resolve Combat"
    #first insure that the action has a valid target
    if not attack.target:
      print "Attack Action has no target, attacking the air in front of you..."
      print "Attack is a success! Three Cheers! Now target something."
      return
    #=============================================================================================
    #Check for relevant status effects which might effect the flow of combat
    # these should be moved to a config file
    # config file should contain classes of status effects
#     cd = {}
#      if False:
#        for stat,mult in ability.multiplier.items():
#          if stat in combatdict:
#            combadict[stat] *= mult        
#        for stat,summand in ability.summand.items():
#          if stat in combatdict:
#            combatdict[stat] += summand 
  #===============================================================================================
    #resolve the defence, and apply the results
    result = self.resolve_defense( attack )
    attack.actor.use ( attack.energy ) #attacker uses the attack, energy is subtracted
    attack.target.use( result['defence'].energy )#defender uses the defence, null actions remove 0

    if result['wounds']:
      attack.target._wounds.append( result['wounds'] )
    print "Attacker Energy: %s " % (attack.actor.energy)
    print "Defender Energy: %s " % (attack.target.energy)
    print "Defense Result: ", result
 #================================================================================================
  def resolve_defense(self, attack ):
    """
      calculate the result of a target's defense (re)action to the attack action
      INPUT:
           -attack: the attack action being performed
      OUTPUT: dictionary with the following keys
               reaction: the reaction 'chosen' by the defender (parry, dodge or block)
               success: True/False if the reaction was successful/unsuccessful
                        a parry or dodge is successful if the attack is evaded, a block is 
                        successful if the attack lands on armour, even if a wound is incurred
               cost: the energy cost to the defender given the chosen action 
               wound: the wound (if any) caused by the attack
    """
    defence = attack.target.mind.getreaction()
    success = False 
    wound = None

    #1. handle defence
    if not (not defence or defence.type=='null'): #if the target defends
      if defence.match( attack.targetnumber() ):  #2. handle a possibly successful defence action
      #   if it is possible to set the defences energy to match the attack's target number
        success = True #then defence is a success
        print "attacker energy",attack.actor.energy()
        #TODO pass the successful defence to the attack object, and see what it says
        #some skills have a trigger on successful defences
    #3. handle unsuccessful defence by resolving armour penetration and any resulting  wounds
    if not success: #resolve_block, can always block, just like you can always get hit it the face
      #TODO work out armour coverage
      #
      if False: #self.armour_hit( cd['dcov']  ):
        self.armour_penetration( attack )
      print "FUCKED IN THE FACE!"
      wound = self.wound_resolution( attack )
    result = { 'defence': defence,
               'success': success,
               'wounds'  : wound }


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
      sets the energy cost of the defence

      OUTPUT: tuple containing pass/fail result of parry, and cost

      ALGORITHM
       every attack skill has a function which calculates a target number as a function of
       energy
       in order to succeed, a defender must be able to spend at least 
    """
    #check parry rules to make sure everything is kosher
    targetnumber = attack.skill.targetnumber( attack.energy ) #the number to beat
    defence.energy = targetnumber #set the energy cost of the defence
    if targetnumber <= defence.skill.targetnumber( attack.target._energy ): 
      return True #defence is successful
    return False  #defence is unsuccessful
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
  def armour_penetration( self, action ):
    """
    """
    return False
  
  #===============================================================================================
  def wound_resolution ( self , action  ):
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
