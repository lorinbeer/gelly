#=================================================================================================
#  maxenergy.py
#    collection of functors designed to represent the various formulae for calculating the max
#    energy attribute of a skill
#
#  justification
#    max energy attribute of a skill is typically a function of the skill level and the skill
#    user's stats. All of these factors are subject to change at any time, and the specific 
#    function used depends entirely on the skill. If we were to statically generate the max energy
#    value when the skill was created, it would mean having to recreate a character's entire skill
#    set every time any stat changes (as we do not know which stat might apply to which skill).
#    Rather than clutter the skill class with a function for every possible formula for 
#    calculating max energy, a given instance of a skill contains a single function object 
#    which calculates the max energy stat for the skill. In this way, if a stat changes, we can
#    both check to see if the stat is relevant to the max energy stat of the skill and update the
#    max energy stat by consulting with the Skills maxenergy functor. We can assign/reassign
#    max energy functors to skills without modifying the code of either.
#
#=================================================================================================
#      default method for calculating the maximum energy of a skill: 
#      f(S,M) = s1*m1 + s2*m2 + ... + sn*mn
      
#      Using this method, the maximum energy 

#=================================================================================================
class SumOfProducts(object):
  """

  """
  def __init__(self,li):
    """
      Initialize the object given a list of tuples. Each tuple should consist solely of strings, 
      representing variables, or numeric constants. 

      INPUT:
           -li: should consist of a list of tuples
 
    """
    self._variables = []
    for tup in li:
      for term in tup:
        if isinstance(term,string):
  def __call__( self, **kwargs ):
    """
      Calculates the Sum of Products determined during initialization. 

      Each term of the sum is the product of the contents of one of the tuples passed to this
      instance during initialization.

      INPUT:
        kwargs: should be dictionary containing the variables passed to this function during
                initialization as keys, and the desired numeric values of each argument as values.
    """
#=================================================================================================
class ProductOfSums(object):
  """
  """
  def __init__(self,**kwargs):
    """
    """
  def __call__(self):
    """
    """

#=================================================================================================
