#=================================================================================================
import sys
sys.path.append("/home/lorin/projects/gelly/objs")
import actor
import pysdlutil

#=================================================================================================
from character.character import Character
from character.controller import Selection, Controller
from character.skill import Skill, SkillFactory
#=================================================================================================
from dungeon.dungeon import DungeonMap, DungeonDecorator
from dungeon.dungeongenerator import DungeonGenerator
from dungeon.dungeonmaster import DungeonMaster
#=================================================================================================
from character.effect import Effect

import os


dg = DungeonGenerator(10,64)
dungeon = dg.generate()

decorator = DungeonDecorator()
pc = decorator.decorate(dungeon)
controller = Controller( pc )
selection = controller._selection

dungeonmaster = DungeonMaster(dungeon)

b = Character("Hardeep", 
              "/home/lorin/projects/ge/art/planetcute/Character Boy.png",
              None,
              [])

def drw():
  pcloc= dungeon.loc( pc )
  dungeonmaster.update()
  dungeon.draw( pcloc )
  selection.draw()
  pos = actor.Vertex()
def drwsel():
  pcloc = dungeon.loc( pc )
  dungeon.draw( pcloc, True )
def keypress( event ):
  controller.interpret( event, dungeon )
  dungeonmaster.turn()
  dungeonmaster.update()
  


