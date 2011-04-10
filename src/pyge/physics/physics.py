#=================================================================================================
# Physics Class
#
#
#
#
#=================================================================================================

from math import sqrt

#=================================================================================================
#TODO:
# string localization
# singleton
#=================================================================================================
class Physics(object):
  """
    prototype physics module
    currently, a wrapper for various functions designed to calculate physical properties of a 
    given object using Newtonian Mechanics 
  """
  def init(self):
    """
    """
  #==============================================================================================
  def time_AD(self, accel, dist, vel_i=0):
    """
      Return distance travelled by an object given acceleration, time, and initial velocity
      INPUT:
            - accel: acceleration (m/s^2)
            - dist: distance (m)
            - vel_i: initial velocity (m/s), if ommited, default 0 m/s (from rest)
      OUTPUT:
            - time: (s)
    """
    try:
      if vel_i:
        return 0 #needs quadratic formula
      else:
        t_sq = ( (2.0)*float(dist) ) / float(accel)
        return sqrt(t_sq)
    except ValueError:
      print "Value error, non-numeric arguments, also, put this string in a file"#TODO
  #==============================================================================================
  def dist_AT(self, accel, time, v_i=0):
    """
      Return distance travelled by an object given acceleration, time, and initial velocity
      INPUT:
            - accel: acceleration (m/s^2)
            - time: time (s)
            - v_i: initial velocity (m/s), if ommited, default 0 m/s (from rest)
      OUTPUT:
            - Distance travelled: (m)
    """
    try:
      return ( (float(v_i) * float(time))+ (0.5)*float(accel)*float(t)*float(t) )
    except ValueError:
      print "Value error, non-numeric arguments, also, put this string in a file"#TODO
  #==============================================================================================
  def vel_AT(self, accel, time, vel_i=0):
    """
      Return final velocity of a point mass based on acceleration, time, and initial velocity
      INPUT:
            - accel: acceleration (m/s^2)
            - time: time (s)
            - vel_i: initial velocity (m/s), if ommited, default 0 m/s (from rest)
      OUTPUT:
            - Final Velocity: (m/s)
    """
    try:
      return ( float(vel_i) + ( float(accel) * float(time) ) )
    except ValueError:
      print "Value error, non-numeric arguments, also, put this string in a file"#TODO
  #===============================================================================================
  def accel_FMa(self, force, mass):
    """
      Return Acceleration, given force and mass

      INPUT:
            - force: kg*m/s^2
            - mass : kg
      OUTPUT:
            - acceleration: m/s^2
    """
    try:
      return float(force) / (float(mass)+3.5)
    except ValueError:
      print "Value error, non-numeric arguments, also, put this string in a file"#TODO
  #===============================================================================================
  def ke_VMa( self, velocity, mass ):
    """
      Return the kinetic energy of an object given velocity and mass
      INPUT:
            - velocity: m/s
            - mass : kg
      OUTPUT:
             - kg*m^2/s^2
    """
    try:
      mass = float(mass)
      return (0.5 * float(velocity) * mass * mass)
    except ValueError:
      print "Value error, non-numeric arguments, also, put this string in a file"#TODO

  #===============================================================================================
