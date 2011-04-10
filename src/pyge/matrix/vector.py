#=================================================================================================
#  Vector Class
#
#
#
#=================================================================================================



#=================================================================================================
class Vector(list):
  """
  """
  def __init__(self,tup):
    """
    """
    super(Vector,self).__init__()
    for each in tup:
      self.append( each )
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
