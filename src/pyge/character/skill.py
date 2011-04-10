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

from action import Action

#=================================================================================================
class SkillInterface(object):pass



class Skill(object):
  """
    Describes a specific ability available to characters and game objects.

    This description defines the skill's level (the relative strength of the ability), the cost 
    to use, requirements to learn, rules limiting how/when the skill is used, the effect the use 
    of the skill has, etc. 
                
  """
  default_lvl_range = (0,5)
  default_threshold = 2.0
  def __init__( self, **kwargs ):
    """
      Initialize the Skill Template. Only the skills name is necessary, all other fields revert to
      default values as defined by the Skill ruleset.
      INPUT:
        name : string representation of this skill's name
        level : the level of this skill
                default: to lower bound of skill level range, defined as a static member
        threshold: minimum energy cost to activate this skill as a number
                   default: default_threshold, static member of this class
        prerequisite: list of skills which must be learned to unlock this skill
                      this skill with level= level-1 is always considered a prerequisite
        
        requirements: list of conditions necessary for this skill to be used as a list of clauses
                      each clause describes a specific state, usually of the character using the
                      skill or the skills target. ie rules for when and how the skill can be used
        damagetype: string damage type. Only relevant for attack skills                    
    """
    try:
      self._name = kwargs['name'] #all skills must a name
      #self._lvlrange = kwargs.get('levelrange',default_lvl_range)
      self._level = kwargs.get('level',Skill.default_lvl_range[0] )
      self._stype = kwargs.get('stype',Action.actype['null'])
      self._threshold = kwargs.get('threshold',Skill.default_threshold)
      self._damagetype = kwargs.get('damagetype',None)
      self._prerequisite = kwargs.get('prerequisite',self._name)
      
      #set up the maximum energy formula
#      self._meformula = {} 
#      for clause in kwargs.get( 'maxenergy', [ ('skill' , 1.0) ] ):
#        self._meformula[ clause[0] ] = clause[1]
      self._energy = self._threshold #
      self._maxenergy = self.calcmaxenergy()
      self._requirements = kwargs.get('requirements',None)
      self._effect = kwargs.get('effect',None)
    except KeyError:
      print "Neccesary argument for class Skill not present"
      raise KeyError
  #===============================================================================================
  def name(): return self._name
  def level(): return self._level
  #===============================================================================================
  def calcmaxenergy( self , **kwargs ):
    """
      Calculate and update the maximum energy stat of this skill
      Currently is calculated with me = threshold+level
    """
    return  self._threshold + self._level
#    self._maxenergy = 0.0
#    for key,value in self._meformula.values():
#      self._maxenergy += kwargs[key]
#    self._maxenergy 
  #===============================================================================================
  def get_effect(self):
    """
      Return the effect of this skills use
    """
    return self._effect
  #===============================================================================================
  def setenergy(self,energy):
    """
      Set the amount of energy to use with this skill

      Behaviour: if energy does not meet threshold, return 0
                 if threshold<=energy<=max_energy, energy to use with this skill is set to argument
                 if energy exceeds max energy, energy to use with this skill is set to max_energy
      INPUT : energy, integer value
      OUTPUT: value set to energy, as per behaviour
    """
    if energy < self._threshold: #energy does not meet threshold
      return 0  #do nothing
    elif energy <= self._maxenergy: #energy within allowed range
      self._energy = energy 
    else: #energy exceeds maximum
      self._energy = self._maxenergy 
    return self._energy
  #===============================================================================================
  def getenergy(self): 
    """return the current value of energy"""
    return self._energy
  #===============================================================================================
  def targetnumber(self):
    """
      Target Number
    """
    return self._energy #+ self._
  #===============================================================================================
  def skilltype(self):
    """
      Return the skilltype of this skill
    """
    return self._stype
  #===============================================================================================
  def __str__(self):
    """
    """
    return "%s" % (self._stype)
#=================================================================================================



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
    self._effectypes={'Null': [Null], }
    self._skilltemplates={'slash': {'levelrange':(0,5), 
                                    'threshold' : 2,
                                    'maxenergy' : None,
                                    'prereqs'   : None,
                                    'effect'    : None },
                          'thrust': {'levelrange':(0,5),
                                     'threshold' : 2,
                                     'maxenergy' : None,
                                     'prereqs'   : None,
                                     'effect'    : None },
                          'strike': {'levelrange':(0,5),
                                     'threshold' : None,
                                     'maxenergy' : None,
                                     'prereqs'   : None,
                                     'effect'    : None },
                          'spin': {'levelrange':(0,5),
                                     'threshold' : None,
                                     'maxenergy' : None,
                                     'prereqs'   : None,
                                     'effect'    : None },
                          }


  def skill(self,sid):
    """
    """
    if sid not in self._skilltemplates: return False
    
    s = Skill()
    setattr
    s.name = self._skills[sid]
  def register_skill(self, template, **kwargs ):
    """
      Register a new skill with the factory.
    """
    
  def register_template(self):
    """
      Register a new skill template with the factory.

      A skill template is a pattern for creating a wide range of individual skills.
      Registering a new template should only be done if the current space of skills that can be
      created with existing templates does not cover a new desired skill
    """

#=================================================================================================
class Ability(object):
  """
    represents a specialized action useable by a game object to interact with the game environment
  """
  def __init__(self, character, base_id):
    """
      character : the character to which this ability belongs
      base_id   : the db id tag of this ability, used to load base attributes
    """
    
    #query db to initialize the object
     #name of this ability
    self._name   = None
     #effect that this ability has if successful, can be status effects, debuffs, etc
    self._effect = None 
     #modifiers that this ability has to the flow of combat, 
    
     #ability multipliers
    self.multipier = dict()
     #ability summands
    self.summand = dict()
#=================================================================================================
