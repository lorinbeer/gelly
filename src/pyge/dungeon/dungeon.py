#=================================================================================================
# Dungeon Map Class
#
#
#
#=================================================================================================
import sys
sys.path.append("/home/lorin/projects/gelly/objs")
#=================================================================================================
from actor import Actor, Animactor
from actor import Vertex, Vertel, IntVec
from util.vector import Vector


from character.effect import Effect

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

    self._itemoffset = Vertex()
    self._itemoffset.append (0.0)
    self._itemoffset.append (0.0)
    self._itemoffset[1] = 0.054
#    super(Tile,self).__init__( model   = [ (0,0), (0,181), (100,181), (100,0) ],
#                               texture = self.tiletypes[tilecode],
#                               x = 100,
#                               y = 85,
#                               boundoffset = (0,44) )
    _model = Vertel()
    _model.set( [ ( 0.0, 0.0, 0.0 ), 
                  ( 0.0, 171.0/600.0, 0.0 ), 
                  ( 101.0/800.0, 171.0/600.0,0.0 ),
                  ( 101.0/800.0 , 0.0, 0.0 ) ] )
    _bound = Vertel() 
    _bound.set( [ ( 0.0, 0.0, 0.0 ),
                  ( 0.0, 100.0/600.0, 0.0 ),
                  ( 100.0/800.0, 100.0/600, 0.0 ),
                  ( 100.0/800, 0.0, 0.0 ) ] )
    super(Tile,self).__init__( self.tiletypes[tilecode], _model, _bound )


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
    vpos = Vertex()
    vpos.append( pos[0] )
    vpos.append( pos[1] )
    super(Tile,self).draw( vpos )#pos, (self.x,self.y) )
    for each in self.items:
      vpos[0]=vpos[0]+self._itemoffset[0]
      vpos[1]=vpos[1]+self._itemoffset[1]
      if not isinstance(each, Animactor):
        each.draw( vpos )#(pos[0],pos[1]),"object" )
      else:
        each.draw( vpos )

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

  def setWall(self, full):
    """
    """
    self.full = full

  def isWall(self):
    return False
  def isOccupied(self):
    return True

#=================================================================================================
class DungeonMap(object):
  """
  """
  def __init__(self,roguemap=None):
    """
    """ 

    self.size = ( roguemap.x, roguemap.y )
    self._x = roguemap.x
    self._y = roguemap.y
    self.map = dict()
    self.characters = MultiDict( )  #all characters, pc's and npc's currently on the map
    self.gitems     = MultiDict( )  #all game items currently on the map
    self.effects    = MultiDict( )  #all graphic effect objects active on the map

    for i in range(0, roguemap.x ):
      for j in range(0, roguemap.y ):
        self.map[i,j] = Tile( i, j, roguemap.arr[i][j] )
        self.map[i,j].x = i
        self.map[i,j].y = j

    #now that the dungeon map has been created, we can initialize the dungeon actor
    self.tile_size = Vector( (100,81) )
    self.screen_size   = Vector( (800,600) )
    self.screen_center = Vector( (0,0) )
    self.center_tile = Vector( (0,0) )
    self.x_range = Vector( )
    self.y_range = Vector( )
  #===============================================================================================
  def draw(self,center,select=False):
    """
      INPUT:
            -center: tile to render at center
    """
    #=============================================================================================
    xdrawstep = 101.0/800.0
    ydrawstep =  81.0/600.0
    yoffset   = -171.0/600.0

    screencenter=(0.45,0.4)
    x_range = (center[0]-5, center[0]+5)
    y_range = (center[1]-4, center[1]+4)

    xstart = screencenter[0] - 4*xdrawstep
    ystart = screencenter[1] - 2.5*ydrawstep

    ycoord = ystart
    for y in range( 0, 9):
      xcoord = xstart
      for x in range( 10, 0 ,-1):
        tile= (x_range[0]+x,y_range[0]+y)
        if tile[0]<0 or tile[1]<0 or tile[0]>=self._x or tile[0]>=self._y:
          tile=False
        if tile:
          p = IntVec()
          p.append( int(tile[0]) )
          p.append( int(tile[1]) )
          if select: self.map[tile].selectdraw( p )
          else: self.map[tile].draw( (1.0-xcoord,1.0-ycoord) )
        xcoord+=xdrawstep
      ycoord+=ydrawstep
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
    if isinstance(pos,Vector):
      pos = pos.hash()
    if self.map[pos].full: return False

    if isinstance(item,Character):
      self.map[pos].place_item( item )
      self.characters[pos] = item
      print "POSITIONING", pos
    elif isinstance(item,Gitem):
      self.map[pos].place_item( item )
      self.gitems[pos] = item
    elif isinstance(item,Effect):
      self.map[pos].place_item( item )
      self.effects[pos] = item
    print "item %(name)s placed" % {'name': item }
  #===============================================================================================
  def movecharacter( self, character, dest, mode='relative' ):
    """
      reposition a character currently on the map to another location on the map

      if you wish to place a character on the map, use placecharacter instead
      
      this function returns false only if the character is not on the map, or if the destination tile is full
      a full tile generally means a wall
      @param character to move
      @param dest tuple coordinate representing destination/offset, depending on mode
      @param mode: de: relative, or absolute, default is relative
    """
    loc = self.loc(character) #get the location of the character
    if mode == 'relative': dest = dest+loc #calculate destination based on mode
    if loc and not self.map[dest.hash()].full:
      self.characters[loc.hash()].remove(character) #remove character the character list
      self.map[loc.hash()].remove_item( character ) #remove item from tile
      self.map[dest.hash()].place_item( character ) #place item on new tile
      self.characters[dest.hash()] = character #insert item into characters at new loc
  #===============================================================================================
  def loc(self,item):
    """
      if item is on the map, return tuple containing its coordinates, returns false otherwise
    """  
    for each in self.characters.items():
      if item == each[1]:
        return Vector(each[0])
    return False
  
  #===============================================================================================
  def remove(self,item):
    """
      removes the item from the map,
    """
    from character.character import Character
    from gitem.gitem import Gitem
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
    if isinstance(item,Effect):
      for loc,effect in self.effects.items():
        if item == effect:
          self.effects[loc].remove( item )
          self.map[ loc ].remove_item( item )
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
from character.skill import SkillFactory
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
          dungeon.map[(i,j)].setWall(True) #inform this tile that it is a wall

  def decorate(self,dungeon):
    """
    """
    from character.character  import Character
#    from character.controller import Controller
    from gitem.gitem import Gitem,GitemFactory

    self.__placewalls__(dungeon)


    sg = SkillFactory()
    skillslash = sg.makeskill( 'slash' )

    gitemFac = GitemFactory()
    image_pc = "/home/lorin/projects/ge/art/planetcute/Character Horn Girl.png"
    pc = Character("Angelina", image_pc, dungeon, [], 1)
    pc.width = 0
    knife = gitemFac.makegitem()
    pc.mind._disabled = True
    pc.skillbook.learn( skillslash )
    pc.setskill( slot='SLOT_1', skill=skillslash.name )

    image_mob = "/home/lorin/projects/ge/art/planetcute/Enemy Bug.png"
    mob = Character("Goblin", image_mob, dungeon,[],-1)
    mob.health = 25

    image_mob2 = "/home/lorin/projects/ge/art/planetcute/Character Boy.png"
    mob2 = Character("Boy", image_mob2, dungeon,[],-1)
    mob2.health = 50

    dungeon.place( pc,  (5, 0) )
    dungeon.place( mob, (5,15) )
    dungeon.place( mob2, (5, 25) )



 #   image_mob = "/home/lorin/projects/ge/art/planetcute/Character Horn Girl.png"
 #   mob = Character("badgirl", image_mob, dungeon)
 #   mob.health = 25
 #    dungeon.place( mob, (5,25) )


 #   image_mob = "/home/lorin/projects/ge/art/planetcute/Character Boy.png"
 #   mob = Character("badboy", image_mob, dungeon)
 #   mob.health = 25
 #   dungeon.place( mob, (5,35) )





    #give each character a weapon
    knife = gitemFac.makegitem()
    pc.weapon = knife
    knife = gitemFac.makegitem()
    mob.weapon = knife
    return pc
