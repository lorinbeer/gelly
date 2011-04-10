#=================================================================================================
# Buffable Class
#  module (attachable to game object) which allows object to be buff'ed/debuff'ed
#
#=================================================================================================

# how this works
# keeps track of all temporary buffs/debuffs placed on the object
#  communication between parent object and module ie object/module interface
#  


# TODO: implement the _buffs list as a priority queue


#=================================================================================================
class Buffable(object):
  """
  """
  def __init__(self,obj):
    """
      
      obj - the object this instance of Buffable will interact with
    """
    self._obj = obj      # object this instance of Buffable is bound to
    self._buffs = list() # list of buffs active on the target  
  # 
  #===============================================================================================
  def buff(self, stat, mod, time):
    """
      apply a buff (stat modifier) to the object registered with this object
      stat - statistic of the registered object to modify
      mod  - modifier to apply to the stat
      time - the number of turns the buff should be active for
    """
    try:
      self._obj[stat] += mod  #apply the mod
      self._buffs.append( {key:stat,mod:mod,time:time}) #add the mod to
    except keyerror: 
      print "object does not have %(st)s to (de)buff)" %{st:stat}
  #===============================================================================================
  def update(self):
    """
      update the buff list, removing any expired buffs
    """
    for i,buff in enumerate(self._buffs.reverse() ): # go through buffs from oldest to youngest
      buff[time] -= 1      # decrement buff time counter
      if buff[time] <= 0:  # if we've reached zero
        self._obj[ buff[stat] ] -= buff[mod] #reverse the effect of the buff
        self._buffs.pop(i) # and remove the buff

        
    
#=================================================================================================
