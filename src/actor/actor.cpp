//================================================================================================
//
//
//
//
//================================================================================================

#include "actor.h"
#include <iostream>
#include <vector>
//================================================================================================

unsigned int topname=0;
unsigned int NAME_GEN(){
  return ++topname;
}

//================================================================================================
int default_model_init( Vertel & model )
{
  if ( INIT_VERTEX_LIST( model, 4, 3 ) ) {
    model[0][0] = 0.f;
    model[0][1] = 0.f;
    model[0][2] = 0.f;

    model[1][0] = 0.f;
    model[1][1] = 171.0f/600;
    model[1][2] = 0.f;

    model[2][0] = 101.0f/800;
    model[2][1] = 171.0f/600;
    model[2][2] = 0.f;


    model[3][0] = 101.0f/800;
    model[3][1] = 0.f;
    model[3][2] = 0.f;
    return 1;
  }
  else {
    return 0;
  }
}
int default_bounding_model_init( Vertel & model )
{
  if ( INIT_VERTEX_LIST( model, 4, 3 ) ) {
    model[0][0] = 0.f;
    model[0][1] = 0.f;
    model[0][2] = 0.f;

    model[1][0] = 0.f;
    model[1][1] = 80.0f/600;
    model[1][2] = 0.f;

    model[2][0] = 100.0f/800;
    model[2][1] = 80.0f/600;
    model[2][2] = 0.f;

    model[3][0] = 100.0f/800;
    model[3][1] = 0.f;
    model[3][2] = 0.f;
    return 1;
  }
  else {
    return 0;
  }
}
//================================================================================================
Actor::Actor(  char const * texpath/*, void*model */ ):
  model(),
  boundmodel(),
  boundoffset(),
  boundpos(),
  pos(),
  name( NAME_GEN() ),
  texid(0),
  drawmode(0),
  offset(0)
{
  default_model_init(model);
  default_bounding_model_init(boundmodel);
  INIT_VERTEX( boundoffset, 3 );
  INIT_VERTEX( boundpos   , 3 );
  INIT_VERTEX( pos, 3 );
  boundoffset[1] = 42.0/600.0;

  boundpos[0] = pos[0]+boundoffset[0];
  boundpos[1] = pos[1]+boundoffset[1];

  //try
  Graphics * gfx = Graphics::Instance();
  texid = gfx->loadtexture( texpath ); 
}
//================================================================================================
void Actor::draw(){
  Graphics * gfx = Graphics::Instance();
  gfx->draw( this->model, this->pos, this->texid );
  //gfx->draw( this->boundmodel, this->boundpos );
}
void Actor::selectdraw( std::vector< int > & _name ){
  Graphics * gfx = Graphics::Instance();
  gfx->addselect( this->getdrawitem(_name) );
}
//================================================================================================
void Actor::setpos(Vertex const & npos){
  /*  if ( npos.size() == this->pos.size() ){
    this->pos = npos;
    }*/
  this->pos[0] = npos[0];
  this->pos[1] = npos[1];
  this->boundpos[0] = this->pos[0] + this->boundoffset[0];
  this->boundpos[1] = this->pos[1] + this->boundoffset[1];
  //  printf("pos %f %f npos %f %f  \n",pos[0],pos[1], npos[0], npos[1]);
}
void Actor::setpos(float x, float y, float z){
  float npos[]= {x,y,z};
  this->pos.assign(npos,npos+3);
  this->boundpos[0] = this->pos[0]+ this->boundoffset[0];
  this->boundpos[1] = this->pos[1]+ this->boundoffset[1];
}
//================================================================================================
DRAW_ITEM *Actor::getdrawitem( std::vector< int > & _name ){
  DRAW_ITEM * drawitem = new DRAW_ITEM;
  drawitem->name  = _name;
  drawitem->model = &(this->boundmodel);
  drawitem->pos   = &(this->boundpos);
  return drawitem;
}
//================================================================================================

