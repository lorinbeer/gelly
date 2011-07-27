#=================================================================================================
#  Formulas
#    to maintain flexibility, skills use lambda functions for their various calculations
#    the lambda function to use is specified by a variable it is bound to
#
#    Adding New Skills
#      if you wish to add new skills
#
#    Alternate Skill Set
#      TODO: add ability to change where skills are loaded from
#
#    Writing New Formulas
#      1. No sanity checks are required unless as part of the formula, eg the Skill object will
#         insure that the threshold is met before calling the target number formula
#
#=================================================================================================
#=================================================================================================
#formulas

#MAXIMUM ENERGY FORMULAS
DEFAULT_MAXENERGY_FORMULA = lambda skill,character: skill.level+skill.threshold

#DEFAULT TARGET NUMBER FORMULAS
DEFAULT_TARGETNUMBER_FORMULA = lambda skill,character,energy: energy-skill.threshold+1

#DEFAULT MATCH FORMULAS
DEFAULT_MATCH_FORMULA = lambda skill,character,tn: tn+skill.threshold-1

#DEFAULT BEAT FORMULAS
DEFAULT_BEAT_FORMULA = lambda skill,character,tn: tn+skill.threshold

#DEFAULT ON SUCCESS FORMULA
# called when skill successfully passes a skillcheck
DEFAULT_ONSUCCESS_FORMULA = lambda action,character: False

#DEFAULT ON FAIL FORMULAS
# called when a skill fails to pass a skillcheck
DEFAULT_ONFAIL_FORMULA = lambda action,character: action.setenergy( action.maxenergy() )
