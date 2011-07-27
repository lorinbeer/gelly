#=================================================================================================
# Energy Class
#  models the energy stat
#  
#
#=================================================================================================



#=================================================================================================
class Energy(object):
  """
    utility class to model energy stats of character objects

    Class Energy is independent from the classes that use it, but it really only makes sense 
    within the context of Character classes. IE this class is generally not very reuseable, it
    implements a rather specific set of game rules.

     
    Health - measure of how near death a character is 
    Pool   - energy resevoir
    Hand   - available energy subpool available at any given moment
    
    
  """
  def __init__(self):
    """

    """
    self._healthmax = 100
    self._health = 0
    self._poolmax = 100
    self._pool = self._poolmax
    self._handmax = 10
    self._hand = self._handmax
  #===============================================================================================
  def subhand(self, amount, tomin=False):
    """
      expend energy from hand, reducing energy in hand by amount. If there is not enough energy
      in the hand than we return false and do not subtract any energy unless tomin is specified
    """
    fhand = self._hand - amount
    if fhand < 0:
      if tomin: self._hand = 0
      return False
    self._hand = fhand
    return fhand
  #===============================================================================================
  def rechargehand(self, amount=None):
    """
      Refill hand from pool by amount to the allowed maximum. 
      INPUT: -amount: the amount to add to the hand, if None then attempt to add the max amount
      OUTPUT: -the amount added to pool
    """
    if not amount: amount = self._handmax
    fhand = self._hand + amount      #fill hand by amount
    overflow = fhand - self._handmax #overflow: attempting to add more to the hand than allowed
    if overflow > 0:
      amount = self._handmax - self._hand
    underflow = self._pool - amount #underflow: attempting to remove more from pool than allowed
    if underflow < 0:
      amount += underflow 
    self._hand += amount
    self._pool -= amount
    return amount
  #===============================================================================================
  def rechargepool(self, amount):
    """
      Add amount to pool 
    """
    self._pool += amount
    overflow = self._pool - self._poolmax
    if overflow > 0:
      amount -= overflow
      self._pool = self._poolmax
    return amount
  #===============================================================================================
  #===============================================================================================
  def __str__(self):
    """
    """
    return "Energy: Pool=, %i  Hand= %i" % (self._pool, self._hand)
#=================================================================================================
