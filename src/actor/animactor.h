//================================================================================================
//  Animactor Class
//
//
//
//
//================================================================================================
#ifndef _ANIMACTOR_H_
#define _ANIMACTOR_H
//================================================================================================
#include <vector>
#include <list>
#include <string>
#include <SDL/SDL.h>
//#include "actor.h"
#include "graphics.h"
#include <stdio.h>
//================================================================================================
class Animactor: public Actor
{
  public:
  Animactor( std::vector< std::string > & assetpaths, const Vertel & _model ):
    Actor(),
    currentframe(0)
  {
    frames.resize( assetpaths.size() );
    for( int i = 0; i < assetpaths.size(); i++ ){
      frames[i] = Graphics::Instance()->loadtexture( assetpaths[i].c_str() );
	}
    texid = frames[0];
    repeat = 1;
    done =  false;
    model = _model;
  }
  //==============================================================================================

  //==============================================================================================
  void draw( Vertex const & npos )
  {
    Actor::draw( npos );
    this->done = this->update();
  }
  //==============================================================================================
  bool update(){
    currentframe++;
    if ( currentframe >= frames.size() ){
      currentframe = 0;
      if (repeat == 1) {
        return true;
      }
    }
    texid = frames[currentframe];
    return false;
  }
  //==============================================================================================

  //==============================================================================================
  //==============================================================================================
  private:
  std::vector< unsigned int > frames;
  int currentframe;
  int repeat;
  bool done;
  friend class PyAnimactor;
};
//================================================================================================
/*
class Animactor: public Actor
{
  public:
  //==============================================================================================
  //Animactor(){;}
 Animactor( std::vector< std::string > assetpaths ): //Actor("none")
   Actor::Actor(){
   printf("HAFFFFFFFFFFFFFFFF\n");
	     
   // frames.resize( assetpaths.size() );
   //   for( int i = 0; i < assetpaths.size(); i++){
   //     frames[i] = Graphics::Instance()->loadtexture( assetpaths[i].c_str() );
   //  }
   //  last_update = SDL_GetTicks();
   //   texid = frames[0];
  }
  //==============================================================================================
  void draw( ){
    this->update();
    
  }
  //==============================================================================================

  //==============================================================================================
  protected:
  //==============================================================================================
  std::vector< unsigned int > frames;
  int currentframe;
  unsigned int last_update;
  //==============================================================================================
};
//================================================================================================
*/
#endif
