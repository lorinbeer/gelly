
import sys
sys.path.append("/home/lorin/projects/gelly/objs")
import actor
import pysdlutil

from character.character import Character
from character.controller import Selection
#=================================================================================================
# 
from dungeon.dungeon import DungeonMap, DungeonDecorator
from dungeon.dungeongenerator import DungeonGenerator
from dungeon.dungeonmaster import DungeonMaster
#=================================================================================================

dg = DungeonGenerator(10,64)
dungeon = dg.generate()

#
decorator = DungeonDecorator()
pc = decorator.decorate(dungeon)
#selection = pc.controller.selection

#dungeonmaster = DungeonMaster(dungeon)




b = Character("Hardeep", 
              "/home/lorin/projects/ge/art/planetcute/Character Boy.png",
              None,
              [])

def drw():

  dungeon.draw( (0,0) )
 # a.draw()
  pos = cactor.Vertex()

def drwsel():
  #print "draw select"
  dungeon.draw( (0,0), True )

def keypress( key, mod ):
  """
    
  """
  print "key pressed:", key, mod
