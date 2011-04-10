#=================================================================================================
#  DungeonGenerator Class
#
#
#
#   1. Fill the whole map with solid earth
#   2. Dig out a single room in the centre of the map
#   3. Pick a wall of any room
#   4. Decide upon a new feature to build
#   5. See if there is room to add the new feature through the chosen wall
#   6. If yes, continue. If no, go back to step 3
#   7. Add the feature through the chosen wall
#   8. Go back to step 3, until the dungeon is complete
#   9. Add the up and down staircases at random points in map
#  10. Finally, sprinkle some monsters and items liberally over dungeon 
#
#
#
#=================================================================================================

from dungeon import DungeonMap

from other.euclid import Vector2

#=================================================================================================

class RogueMap(object):
  """
    matrix storing a Rogue-like dungeon map
  """
  def __init__( self, x=128, y=128 ):
    """
      
    """
    import sys
    self.x = x
    self.y = y
    self.arr = [ None ]*self.x

    for i,v in enumerate(self.arr):
      self.arr[i] = ['#']*self.y

  #===============================================================================================
  def __str__(self):
    """
            
    """
    s = list()
    for row in self.arr:
      s.append( ''.join(row) )
    return '\n'.join(s)

  #===============================================================================================
  def insert(self,rmap,x0,y0):
    """
    pp  insert the given map into this map, starting at the topleft corner of the submap, and at 
      x,y of the parent map.
      If rmap is larger than this map, insertion will continue until the bounds of this map have
      been reached
      rmap - the submap to insert into this map
      x - x coordinate of cell to begin the insertion
      y - y coordinate of cell to begin the insertion
    """
    i = x0; j = y0
    if x0+rmap.x > self.x or y0+rmap.y > self.y:
      return False
    for row in rmap.arr:
      for e in row:
        self.arr[i][j] = e
        j+=1
      i+=1
      j=y0    
    
#=================================================================================================

class Wall(object):
  """
  """
  def __init__( self, point1, point2, normal ):
    """
    """
    self.p1 = point1
    self.p2 = point2
    self.norm  = normal

#=================================================================================================
class DungeonRoom(RogueMap):
  """    
  """

  def __init__( self, x = 10 , y = 10 ):
    """
    """
    super(DungeonRoom,self).__init__(x,y)
    #create a room by hollowing out the center
    for i in range(1,self.x-1):
      self.arr[i][1:self.y-1] = ['.']*(self.x - 2)
    #store the rooms' walls
    self.walls = list()
    self.walls.append( Wall( (0,0), (x,0), (0 , 1) ) ) #north wall
    self.walls.append( Wall( (x,0), (x,y), (1 , 0) ) ) #east wall
    self.walls.append( Wall( (0,y), (x,y), (0 ,-1) ) ) #south wall
    self.walls.append( Wall( (0,0), (0,y), (-1, 0) ) ) #west wall
  #===============================================================================================
  def __str__(self):
    """
      
    """
    s = list()
    for row in self.arr:
      s.append( ''.join(row) )
    return '\n'.join(s)
  #===============================================================================================


#=================================================================================================
class DungeonGenerator( RogueMap ):
  """
    Proceduraly generates a dungeon map
  """
  def __init__( self, x, y ):
    """
    """
    super(DungeonGenerator,self).__init__(x,y)
  def generate( self ):
    """
    """
    q = list() #list to be used as a queue
    #generate a room and place at center
    room = DungeonRoom( 10, 10 )
    center = ( self.x/2, self.y/2 )
    self.insert( room, center[0]-5, center[1]- 5 )
    self.insert( room, center[0]-5, center[1]-20 )
    self.insert( room, center[0]-5, center[1]-10 )
    self.insert( room, center[0]-5, center[1]+20 )
    self.insert( room, center[0]-5, center[1]-30 )
    #
    q.extend( room.walls ) #add the walls of the room to the queue
    #prune the queue of shared walls
    #create a hallway
    self.arr[ self.x/2 ] = ['.']*self.y
    
    self.arr[5][0] = 'x'
    self.arr[5][-1] ='e'
  
    print self


    return DungeonMap( self ) #initialize the entire map
    

#=================================================================================================

#generate room
#place room at center of dungeon
#add walls of room to queue
#for each wall
# in wall normal, 
