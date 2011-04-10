#=================================================================================================
# Dungeon Map Class
#
#
#
#=================================================================================================
import sys
sys.path.append("/home/lorin/projects/gelly/objs")
#=================================================================================================
from actor import Actor
from actor import Vertex
#from actor.boundedactor import BoundedActor
from matrix.vector import Vector
from other.euclid import Vector2


from itertools import chain,product
#=================================================================================================

#=================================================================================================

class MultiDict(dict):
  """
    dict subclass which stores key/value pairs of the form tuple/object
    suports multiple keys with same value

    a single key tuple can be used to store a coordinate, representing the object's location in
    some coordinate space
    positionrange - legal value range for the key tuples
  """
#=================================================================================================
  def __getitem__( self, key ):
    """
    """
    return dict.__getitem__(self,key)

#=================================================================================================
  def __setitem__(self,key,value):
    """
    """
    super( MultiDict,self ).setdefault( key, [] ).append(value)

  def __delitem__(self,key):
    """
    """
    super( MultiDict,self).__delitem__( key )
#=================================================================================================
  def values(self):
    """
      Generator function, returning all values in the dict
    """
    for val in chain( * super(MultiDict,self).values() ): yield val
#    for l in super(MultiDict,self).values():
#      for each in l:
#        yield each
#=================================================================================================
  def items(self):
    """
    """
#    for k,v in product( super(MultiDict,self).keys(), self.values() ): print k,v
#    for k,v in product( super(MultiDict,self).keys(), self.values() ): yield k,v
#   for k,l in 
    for k,l in super(MultiDict,self).items():
      for each in l:
        yield k,each                    
#
    
#=================================================================================================
  #to support multiple values per key, we need to overload the delete item function
#=================================================================================================


class Tile( Actor ):
  """
  """
  def __init__(self, x, y, tilecode ):
    """
    """
    self._tilecode = tilecode
    self.tile_size = (100,82) #magic, depends on tile set
    # dict of tile type to image path mappings, will eventually be part of DB
    self.tiletypes = { '#' : "/home/lorin/projects/ge/art/planetcute/Stone Block.png",
                       '.' : "/home/lorin/projects/ge/art/planetcute/Stone Block.png",
                       'e' : "/home/lorin/projects/ge/art/planetcute/Wood Block.png",
                       'x' : "/home/lorin/projects/ge/art/planetcute/Wood Block.png"}

    
#    super(Tile,self).__init__( model   = [ (0,0), (0,181), (100,181), (100,0) ],
#                               texture = self.tiletypes[tilecode],
#                               x = 100,
#                               y = 85,
#                               boundoffset = (0,44) )
    super(Tile,self).__init__( self.tiletypes[tilecode] )

    

### subclassed directly from Actor ###
#    model = [ (0,0), (0,181), (100,181), (100,0) ]
#    super(Tile,self).__init__( model, self.tiletypes[tilecode] )


    self.x = x
    self.y = y
    self.items = list()
    
    self.full = False

  def loc(self):
    return tuple([self.x,self.y])
  
  def draw( self, pos = None ):
    """
      draw
    """
#    if self._tilecode == '#':
#      pos = (pos[0],pos[1]+40)
    #super(Tile,self).draw(pos, (self.x,self.y) )
    vpos = Vertex()
    vpos.append( pos[0] )
    vpos.append( pos[1] )
    super(Tile,self).draw( vpos )#pos, (self.x,self.y) )
    for each in self.items:
      vpos[0]=vpos[0]
      vpos[1]=vpos[1]+0.05
      each.draw( vpos )#(pos[0],pos[1]),"object" )
 

  def place_item( self, item ):
    """
      place an object on the tile
    """
    self.items.append( item )

  def remove_item( self, item ):
    """
    """
    self.items.remove( item )#TODO try

  def pop(self):
    """
    """
    self.items.pop()

  def __str__(self):
    """
      debug function, prints class data to console
    """
    str0 =  "Tile Object: %(pos)s \n" % {'pos': tuple([self.x,self.y]),}
    for each in self.items:
      str1 = each.__str__()
      str0 = str0+str1+'\n'
    return str0


#=================================================================================================
class DungeonMap(object):
  """
  """
  def __init__(self,roguemap=None):
    """
    """ 

    self.size = ( roguemap.x, roguemap.y )
    self.map = dict()
    self.characters = MultiDict( )  #all characters, pc's and npc's currently on the map
    self.gitems     = MultiDict( )  #all game items currently on the map 
    

    for i in range(0, self.size[0] ):
      for j in range(0, self.size[1]):
        self.map[(i,j)] = Tile( i, j, roguemap.arr[i][j] )
        self.map[i,j].x = i
        self.map[i,j].y = j

    #now that the dungeon map has been created, we can initialize the dungeon actor
    self.tile_size = Vector( (100,81) )
    self.screen_size   = Vector( (800,600) )
    self.screen_center = Vector( (0,0) )
    self.center_tile = Vector( (0,0) )
    self.x_range = Vector2( )
    self.y_range = Vector2( )
    
  

  def selectdraw(self,center):
    """
    """
    xdrawstep = 101.0/800.0
    ydrawstep =  81.0/600.0
    yoffset   = -171.0/600.0
    for x in range(0,10):
      for y in range(0,10): 
        xpos = float(x)*xdrawstep
        ypos = 1.0 - (float(y)*ydrawstep) + yoffset
        self.map[x,y].selectdraw( )
  #===============================================================================================
  def draw(self,center,select=False):
    """
      INPUT:
            -center: tile to render at center
    """
    xdrawstep = 101.0/800.0
    ydrawstep =  81.0/600.0
    yoffset   = -171.0/600.0
    viewport  = (4,4)   #the range of tiles that should be visible at any given time
    x_range = (center[0]-viewport[0], center[0]-viewport[1])
    y_range = (center[1]-viewport[1], center[1]-viewport[1])
    if x_range[0] < 0: x_range = (0,viewport[0]*2)
#    if x_range[1] > mapsize.x: x_range = (maxx - viewport[0]*2, maxx)
    if y_range[0] < 0: y_range = (0, viewport[0]*2)
#    if y_range[1] > mapsize.y: y_range = (maxy - viewport[1]*2, maxy)
    for x in range(x_range[0],x_range[1]):
      for y in range(y_range[0],y_range[1]):
        xpos = float(x)*xdrawstep
        ypos = 1.0 - (float(y)*ydrawstep) + yoffset
        if select: 
          self.map[x,y].selectdraw()
        else:      
          self.map[x,y].draw( ( xpos, ypos) )
  #===============================================================================================
  def place(self,item,pos):
    """
      place an item on the map 
    """
    from character.character import Character
    from gitem.gitem import Gitem
    #check pos for legal position
    #check character object for appropriate type
    
 #   itemsOnTile = self.characters[pos]
 #   i = itemsOnTile.index( character )

    if self.map[pos].full: return False

    if isinstance(item,Character):
      self.map[pos].place_item( item )
      self.characters[pos] = item
    elif isinstance(item,Gitem):
      self.map[pos].place_item( item )
      self.gitems[pos] = item
    print "item %(name)s placed" % {'name': item.name }
  #===============================================================================================
  def move_character( self, character, dest, mode='relative' ):
    """
      moves a character currently on the map to another location on the map

      item: item to move
      dest: coord destination as a Vector2 object
      mode: relative, or absolute, default is relative
    """
    loc = self.loc(character)
    if mode == 'relative':
      dest = dest+loc

    if self.map[(dest.x,dest.y)].full: return 0

#    if 0 <= dest.x and dest.x < self.size[0] and 0 <= dest.y and dest.y < self.size[1]:  
#      found = False
#      for each in self.characters.items():
#        if each[1] == character:
#          found = True
#          loc   = each[0]

    if True:
      self.characters[loc.x,loc.y].remove(character)
      self.map[loc.x,loc.y].remove_item( character ) #remove item from tile
      self.map[dest.x,dest.y].place_item( character ) #place item on new tile
      self.characters[dest.x,dest.y] = character #insert item into characters at new loc
  #===============================================================================================
  def loc(self,item):
    """
      if item is on the map, return vector2 containing its coordinates, returns false otherwise
    """  
    for each in self.characters.items():
#      print each
      if item == each[1]:
        return Vector2(each[0][0],each[0][1])
    return False
  
  #===============================================================================================
  def remove(self,item):
    """
      removes the item from the map,
    """
    from character import Character
    from gitem import Gitem
    #rare instance of type checking, justified here given that we have organized the different
    #types of items the map can hold into different MultiDicts. This is for efficiency and
    #readability. By typechecking we can provide a unified interface for item manipulation.
    if isinstance(item,Character):
      for char in self.characters.items():
        if item == char[1]:
          self.characters[ char[0] ].remove( item )
          self.map[ char[0] ].remove_item( item  )
    if isinstance(item,Gitem):
      for gitem in self.gitems.items():
        if item == gitem[1]:
          self.gitems[ gitem[0] ].remove ( item )
          self.map[ gitem[0] ].remove_item( item )
  #===============================================================================================
  def calc_range(self,center,screen_range,x_range,y_range):
    """
    """
    x_range[0] =  center[0] - screen_range[0]/2 - 1
    if x_range[0]<0:
      x_range[0] = 0
    x_range[1] =  center[0] + screen_range[0]/2 + 1
    if x_range[1]>self.size[0]-1:
      x_range[1] = self.size[0]

    y_range[0] =  center[1] - screen_range[1]/2 - 1
    if y_range[0]<0:
      y_range[0] = 0
    y_range[1] =  center[1] + screen_range[1]/2 + 1
    if y_range[1]>self.size[1]-1:
      y_range[1] = self.size[1]

  def map2screen(self,pos):
    """
      given map coordinates pos, returns the screen coordinates
    """
    #calculate how many tiles should be visible on the screen
    xelements = self.screen_size[0] / self.tile_size[0]
    yelements = self.screen_size[1] / self.tile_size[1]

    print pos
    print self.center_tile
    offset = Vector(pos) - self.center_tile
    print offset
    offset = Vector( ( offset[0]*self.tile_size[0], offset[1]*self.tile_size[1] ) )
    print offset
    offset = Vector( ( offset[0]+self.screen_center[0], offset[1]+self.screen_center[1]) )
    print offset


    #self.calc_range(self.center_tile,(xelements,yelements),self.x_range,self.y_range)
    #pos = ( pos[0]-self.x_range[0], pos[1]-self.y_range[0] )
    #pos = ( pos[0]*100, pos[1]*81 )
    return offset

#===============================================================================================
#
#
#
#
#===============================================================================================
from gitem.gitem import Gitem
class DungeonDecorator(object):
  """
    Decorates a dungeon with a collection of preset objects, such as characters, items, etc
    This will eventually evolve into a random map generator
  """
  from dungeon import DungeonMap

  def __placewalls__( self, dungeon ):
    """
    """
    for i in range(0, dungeon.size[0] ):
      for j in range(0, dungeon.size[1]):
        if dungeon.map[i,j]._tilecode == '#':
#          wall = Gitem( model = [ (0,0), (0,181), (100,181), (100,0) ],
#                        texture =  "/home/lorin/projects/ge/art/planetcute/Wall Block Tall.png",
#                        offset = (0,46) )
          wall = Gitem( texture = "/home/lorin/projects/ge/art/planetcute/Wall Block Tall.png" )
          dungeon.place( wall, (i,j) )
    
  def decorate(self,dungeon):
    """
    """
    from character.character  import Character
#    from character.controller import Controller
    from gitem.gitem import Gitem,GitemFactory

    self.__placewalls__(dungeon)


  #  attack = Skill( name= 'slash',
     #               level= 3,
     #               threshold= 2,
   #                 damagetype= 'cut',
      #              effect= Action.actype['attack'] )









    gitemFac = GitemFactory()
    image_pc = "/home/lorin/projects/ge/art/planetcute/Character Horn Girl.png"
    pc = Character("Angelina", image_pc, dungeon)
 #   pc.color = Colors("blue")
    pc.width = 0
    knife = gitemFac.makegitem()
    print pc._equipment.equip( knife )
#    pc.controller = Controller(pc)
    pc.mind._disabled = True




    image_mob = "/home/lorin/projects/ge/art/planetcute/Enemy Bug.png"
    mob = Character("Goblin", image_mob, dungeon)
#    mob.color = Colors("red")
    mob.width = 0
    mob.health = 25
    knife = gitemFac.makegitem()
    print mob._equipment.equip( knife )
    #place character
    dungeon.place( pc,  (5, 0) )
    dungeon.place( mob, (5,15) )


    #knife = gitemFac.makegitem()
    #dungeon.place(knife, (5,5) )

    #knife = gitemFac.makegitem()
    #dungeon.place(knife, (1,2) )

    #give each character a weapon
    knife = gitemFac.makegitem()
    pc.weapon = knife
    knife = gitemFac.makegitem()
    mob.weapon = knife
    print pc._equipment['rhand']
    return pc#,mob  #only return the player character
