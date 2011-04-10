//================================================================================================
//  Dungeon Actor
//   utility class for the python game engine
//   handles drawing of an area of a dungeon around a specified center
//
//
// Author: Lorin Beer
// email : doggerel.verse@gmail.com
//================================================================================================
#ifndef _DUNGEON_ACTOR_H
#define _DUNGEON_ACTOR_H
//================================================================================================
#include "actor.h"
//================================================================================================
#include <vector>
#include <boost/python.hpp>
//================================================================================================
//TileMap Class
// Exposed for use in the python codebase, this should be used by whatever class/function inherits
// or uses the dungeon class
// this has the advantage of making it easy and efficient for the DungeonActor class to draw the
// map, as well as fast lookup for the python
typedef std::vector< std::vector< Tile > > TileMap;
//================================================================================================
class DungeonActor 
{
public:
  //==============================================================================================
  // 
  // ARGS: 
  //  - dict: python dictionary containing actor objects, or actor subclasses
  dungeonactor( void * dict ){;}
  //==============================================================================================
  // draws the dungeon around a specified point
  //  - center: vector of ints containing at least 2 elements representing the center to draw
  //            around
  void draw( std::vector< unsigned int > const & center){;}
  void draw( std::vector< unsigned int > center ){;} //allows other array types to be used
  //==============================================================================================
private:
  //==============================================================================================
  
  //==============================================================================================
};
//================================================================================================
#endif //DUNGEON_ACTOR_H
//================================================================================================
