#=================================================================================================
#  Combat Dictionary Class
#    the combat dictionary is a utility class which contains every piece of information necessary
#    to resolve combat, as defined by the combat system (BattleMaster Class).
#
#
#=================================================================================================



#=================================================================================================
class CombatDict(dict):
  """
    Utility class which contains every piece of information necessary to resolve combat, as 
    defined by the combat system (BattleMaster Class).

    Copying all information relevant to combat from individual classes (attacker, defender, 
    weapons, skills, etc) may seem like an unnecessary extra step. However, by doing this, we
    greatly simplify (to the point of triviality) the application rules which alter how combat is
    resolved. For instance, lets say the use of a particular skill reduces the effective armour
    coverage of the target. Implementation of this skill would require specialized syntax to
    describe the rule to be stored in the skill itself, and interpretation of this syntax by the
    combat system to apply the modifier. Repeat this for every possible stat modification, and we
    have O(n) rules and functions. Instead, every stat is stored in a single dict. Rules stored in
    skills are just pairs of dictionary keys and modifiers. The combat system simply applies the
    modifier to the stat, with no knowledge of who the stat belongs to, or how it might affect 
    combat (all that information is present in the key). In this way, rules for stat modification
    are simple tuples with no requirement other than that the stat exist, and interpretation of 
    rules is reduced to a O(1) dictionary lookup. If a stat is not present in the combat 
    dictionary, we can assume that the given rule simply does not apply.
  """
  



#=================================================================================================
