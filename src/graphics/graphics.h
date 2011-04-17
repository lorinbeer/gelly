//================================================================================================
// Graphics
//
//
//
//================================================================================================

#ifndef _GRAPHICS_H_
#define _GRAPHICS_H_

//================================================================================================
#include <SDL/SDL.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <iostream>
#include <vector>
#include <list>
//================================================================================================

typedef std::vector< float > Vertex;
typedef std::vector< Vertex > Vertel;

inline unsigned int INIT_VERTEX( Vertex &vert, unsigned int dim , bool clear=true);
inline unsigned int INIT_VERTEX_LIST( Vertel &verl, unsigned int size, unsigned int dim );

//================================================================================================
unsigned int INIT_VERTEX( Vertex &vert, unsigned int dim=3, bool clear ){
  if ( clear || vert.empty() ){ //we only initialize a vertex if it does not contain any data
    vert.resize( dim , 0 );
  }
  else{
    return 0;
  }
  return 1;
}
//================================================================================================
unsigned int INIT_VERTEX_LIST( Vertel &verl, unsigned int size, unsigned int dim=3 ){
  if ( verl.empty() ){ //we only initialize a vertex list if it does not contain any data
    verl.resize( size, Vertex(dim,0) );
  }
  else{
    return 0;
  }
  return 1;
}

//================================================================================================
struct DRAW_ITEM{
  std::vector< int > name;
  Vertel const * model;
  Vertex const * pos;
};
//================================================================================================
class Graphics
{
public:
  //==============================================================================================
  static Graphics * Instance();
  //==============================================================================================
  //  loadtexture 
  //
  // INPUT:
  //  path:
  //  reload: if true, reload the texture from file, even if already loaded as a texture
  unsigned int loadtexture( const char * path, bool reload=false);
  //==============================================================================================
  // draw function
  void draw( unsigned int texid );
  //draw: model data only, with no texturing
  void draw( Vertel const&model, Vertex const&pos )const;
  //draw: textured model
  void draw( Vertel const&model, Vertex const&pos, unsigned int texid )const;
  //==============================================================================================
  // render around point, returning names of any object intersected
  unsigned int select( Vertex const & point,
                       std::vector< unsigned int > & name );
  // add an object to select draw list
  void addselect( DRAW_ITEM * ditem ){ if(ditem) selectdraw.push_back( ditem ); }
  //==============================================================================================
private:
  //==============================================================================================
  // private constructor
  Graphics();
  //==============================================================================================
  static Graphics * m_instance;
  //==============================================================================================
  std::list< DRAW_ITEM *> selectdraw;
  //==============================================================================================
  //data relevant to the display
  unsigned int width;
  unsigned int height;
  SDL_Surface * display;
  Vertel texcoords;
};
//================================================================================================
#endif //_Graphics_H_
//================================================================================================
