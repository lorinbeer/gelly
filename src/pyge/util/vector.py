#=================================================================================================
#  Vector Class
#
#
#
#=================================================================================================
from math import sqrt

#=================================================================================================
class Vector(list):
  """
  """
  def __init__(self,elements=()):
    """
    """
    super(Vector,self).__init__()
    for each in elements:
      self.append( each )
#=================================================================================================
  def x(self):
    return self[0]
  def y(self):
    return self[1]
  def z(self):
    return self[2]
#=================================================================================================
  def sub(self,x):
    """
      shorthand element wise subtraction of this Vector by Vector x
      x must be of the same dimension of self
    """
    for i,v in enumerate( self ):
      self[i] = v - x[i]
  def __sub__(self,x):
    """
      returns the result of the element wise subtraction of this Vector by x
      x must be of the same dimension of self
    """
    answer = Vector( self )
    answer.sub(x)
    return answer
#=================================================================================================
  def add(self,x):
    """
    """
    for i,v in enumerate( self ):
      self[i] = v + x[i]
  def __add__(self,x):
    answer = Vector( self )
    answer.add(x)
    return answer

#=================================================================================================
  def div(self,x):
    """
    """
    for i,v in enumerate( self ):
      self[i] = v/x

  def __div__(self,x):
    """
      return Vector representing result of scalar division of this Vector by x
    """
    result = Vector( self )
    result.div(x)
    return result
#=================================================================================================
  def __str__(self):
    """
    """
    return "[%(x)s %(y)s]" % { 'x': self[0], 'y': self[1] }
#=================================================================================================
  def magnitude(self):
    """
    """
    sum=0;
    for e in self:
      sum+=e*e;
    return sqrt(sum);
#=================================================================================================
  def normalized(self):
    mag = self.magnitude();
    for i,e in enumerate(self):
      self[i] = e/mag;
#=================================================================================================
  def hash(self):
    """
    uses tuple representation of Vector as hash value

    Why this isn't stupid: Vectors are 
    """
    return tuple(self)
#=================================================================================================
  def ctint(self):
    for i,e in enumerate(self):
      self[i] = int(e)
#=================================================================================================
