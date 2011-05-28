#=================================================================================================
#  Class SkillBook
#
#
#
#=================================================================================================

from dungeon.dungeon import MultiDict

#=================================================================================================
class SkillBook(MultiDict):
  """
  """
  def __init__(self, **kwargs):
    """
      input:
         "skills": an iterable object containing skill objects
                   currently, any object which implements the name() and level() interface
                   qualifies as a skill
      
    """
    skills = kwargs.get("skills",[]) 
    for s in skills: self[s.name()].s #place all the skills in the dict, keyed by their name
    for k in self.keys(): self[k].sort( key=lambda x: x.level() ) #sort the skills by their level
    #sanity check
    #the result is a dictionary of lists of skills, keyed by the skill. Each key represents all
    #skills of name key. The list should be sorted with increasing level.
  #===============================================================================================
  def learn( self, skill ):
    """
    """
    self[ skill.name ]=skill
  #===============================================================================================


  #===============================================================================================

  #===============================================================================================
#=================================================================================================
