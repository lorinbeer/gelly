#=================================================================================================
# Ability Class
#
#
# Author - Lorin Beer
# email  - doggerelVerse@gmail.com
#=================================================================================================


#so, what can an ability do?
#  provide bonuses to stats for the purpose of calculating combat
#  provide an alternative calculation for combat
#  provide an effect if attack is successful


#  
#    slash, stab, slam
#    thrust (stab)
#    swing  (slash, slam)
#=================================================================================================

#=================================================================================================
#=================================================================================================
import sys
sys.path.append( "/home/lorin/projects/gelly/objs" )
from actor import Animactor
from action import Action
from effect import Effect
#=================================================================================================
#=================================================================================================
class Skill(object):
  """
    Describes a specific ability available to characters and game objects.

    This description defines the skill's level (the relative strength of the ability), the cost 
    to use, requirements to learn, rules limiting how/when the skill is used, the effect the use 
    of the skill has, etc.   
  """

  levelrange = (0,5)

  def __init__( self, **kwargs ):
    """  
    """
    try:
      self.name       = kwargs['name']  #all skills must have a name
      self.type       = kwargs['atype'] #all skills must have an action type
      self.level = kwargs['level']
      self.threshold = kwargs.get('threshold')
#      self.damagetype = kwargs.get('damagetype',None) 
      self.effect = kwargs.get('effect',None)
    except KeyError:
      print "Neccesary argument for class Skill not present"
      print kwargs
      raise KeyError
  #===============================================================================================
  def maxenergy(self):
    """
    """
    return self.level + self.threshold
  #===============================================================================================
  def match(self, targetnumber ): 
    """
      calculate energy as a function of a (hypothetical) target number.
      If this skill can't be raised by the neccesary amount of energy, return false
      
    """
    return targetnumber+1
  #===============================================================================================
  def targetnumber(self,energy):
    """
      calculate the Target Number as a function of the energy to use with this skill. 
      Since a Skill object does not track energy, it must be supplied.
    """
    if energy > self.threshold and energy < self.maxenergy():
      return energy-1
    return 0;
  #===============================================================================================
  def __str__(self):
    """
    """
    return "%s" % (self.name)
#=================================================================================================

import os

class SkillFactory(object):
  """
    Factory class for skills

    Overview:
    To get an instance of a given skill, simply use the skill function
    Skills are created based on templates, the set of all possible skills based on a given
    template is large, and different templates have disjoint sets of possible skills.

    To create a new skill, you simply have to define it in terms of a given template with the
    register_skill function. If the new skill does not fall into an existing template-space, a 
    new template can be defined with the register_template function.

    Templates are implemented as a list, avoiding the need to write code if a new template
    is desired. Each element in the list represents a datamember or function member of skills
    created using this template.
    Example Templates:
      Basic - name: string containing the name of the skill, should be unique
            - level: integer representing the level of this skill
            - threshold: the activation cost of this skill
            - prereqs: list of skill id's representing the prerequisites of this skill
            - effect: the type of effect the use of this skill causes
  """
  def __init__(self):
    """
    """
    #read the data file to register the basic skill types
    self._gfxeffects={'null' : None,
                      'slash': { 'assetpath' :"/home/lorin/projects/ge/art/cut_a",
                                 'framepaths': [] }
                     }
    
    print "init skill factory"
    for k,d in self._gfxeffects.items():
      if d:
        framenames = os.listdir( d['assetpath'] )
        framenames.sort()
        for frame in framenames:
          path = str(os.path.join( d['assetpath'], frame ))
    
          d['framepaths'].append( path )
    print self._gfxeffects['slash']['framepaths']
    eek = Effect( self._gfxeffects['slash']['assetpath'] )
    print eek.done
    self._skilltemplate={ 'slash': {'atype' : 'attack',
                                    
                                    'levelrange':(0,5), 
                                    'threshold' : 2,
                                    'maxenergy' : 5,
                                    'prereqs'   : None,
                                    'effect' : eek
                                   },
                          'thrust': {'atype' : 'attack',
                                     
                                     'levelrange':(0,5),
                                     'threshold' : 2,
                                     'maxenergy' : 5,
                                     'prereqs'   : None,
                                     'effect'    : None },
                          'strike': {'atype' : 'attack',

                                     'levelrange':(0,5),
                                     'threshold' : None,
                                     'maxenergy' : 5,
                                     'prereqs'   : None,
                                     'effect'    : None },
                          'spin':   {'atype'     : 'attack',

                                     'levelrange':(0,5),
                                     'threshold' : None,
                                     'maxenergy' : 5,
                                     'prereqs'   : None,
                                     'effect'    : None },
                          #DEFENCE SKILLS
                          'parry': { 'atype'     : 'parry',                           
                                     'levelrange':(0,5),
                                     'threshold' : None,
                                     'maxenergy' : 3,
                                     'prereqs'   : None,
                                     'effect'    : None },

                          'dodge': { 'atype'     : 'dodge',
                                     'levelrange':(0,5),
                                     'threshold' : None,
                                     'maxenergy' : 3,
                                     'prereqs'   : None,
                                     'effect'    : None }
                                   
                          }
    print "done init skill factory"
  #===============================================================================================
  def makeskill(self,sid,level=0):
    """
    """
    if sid not in self._skilltemplate: return False
    sk = self._skilltemplate[sid]
    sk['name']=sid
    sk['level']=level
    return Skill( **(sk) )
    print "FOOOKAAAH"
#
  #===============================================================================================
  def register_skill(self, template, **kwargs ):
    """
      Register a new skill with the factory.
    """
  #===============================================================================================
  def register_template(self):
    """
      Register a new skill template with the factory.

      A skill template is a pattern for creating a wide range of individual skills.
      Registering a new template should only be done if the current space of skills that can be
      created with existing templates does not cover a new desired skill
    """
  #===============================================================================================
