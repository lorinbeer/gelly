//================================================================================================
//  Graphics.cpp
//    Implementation of Class Graphics.
//    See header file for details.
//
//  If you want to learn how to use this class, your in the wrong place.
//
//
//  Author: Lorin Beer
//
//
//
//================================================================================================
#include <iostream>
#include <stdio.h>

#include "graphics.h"

//================================================================================================

#include "SDL_image.h"



Graphics * Graphics::m_instance = 0;
//================================================================================================

//================================================================================================
Graphics * Graphics::Instance(){
  if ( m_instance == 0 ){
    m_instance = new Graphics();
  }
  return m_instance;
}
//================================================================================================
Graphics::Graphics():
  selectdraw(),
  width(800),
  height(600),
  display(0),
  texcoords()
{
  if (SDL_Init(SDL_INIT_EVERYTHING) < 0){
      //  return 0;
  }
  this->display = SDL_SetVideoMode( this->width, this->height, 32, 
				    SDL_HWSURFACE |SDL_GL_DOUBLEBUFFER | SDL_OPENGL );

  //  glClearColor( 1.f, 1.f, 1.f, 1.f);
  glClearColor( 0.f, 0.f, 0.f, 0.f);

  glClearDepth(1.0f);

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glOrtho(0.f, 1.f, 0.f, 1.f, 0.f, 1.f);
  glViewport(0, 0, 800, 600);
  glMatrixMode(GL_MODELVIEW);
  glEnable(GL_TEXTURE_2D);
  glEnable(GL_BLEND);
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

  glLoadIdentity();



  INIT_VERTEX_LIST( texcoords, 4, 2 );
  texcoords[0][0] = 1.f;
  texcoords[0][1] = 1.f;

  texcoords[1][0] = 1.f;
  texcoords[1][1] = 0.f;

  texcoords[2][0] = 0.f;
  texcoords[2][1] = 0.f;

  texcoords[3][0] = 0.f;
  texcoords[3][1] = 1.f;

}
//================================================================================================



//================================================================================================
// loads image file at path into an opengl texture, returns texture id, returns 0 if fails
unsigned int Graphics::loadtexture( const char * path, bool reload )
{
  SDL_Surface *image = IMG_Load(path);//first load the file into an SDL texture using SDL_image
  unsigned int texture_id; 
  if( image ) {
    glGenTextures(1, &texture_id);           //generate a texture id
    glBindTexture(GL_TEXTURE_2D, texture_id);//and bind it
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
		 image->w, image->h, 0, 
		 GL_RGBA, GL_UNSIGNED_BYTE, image->pixels);
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    SDL_FreeSurface(image);
  }
  else {
    //LOG: image load failed, are you sure the file path is a supported image format?
    return 0;
  }
  return texture_id;//everything went better than expected
}

//================================================================================================
//  draw methods
//
//
//================================================================================================

void Graphics::draw( unsigned int texid ){
  // glLoadIdentity();
  //  glTranslatef( 0, 0, 0);
  glEnable(GL_TEXTURE_2D); // #enable 2d texturing
  glBindTexture(GL_TEXTURE_2D, texid );
  glBegin( GL_POLYGON );
      glTexCoord2f(0.f, 1.f); glVertex3f(0.f, 0.f, 0.f);
      glTexCoord2f(0.f, 0.f); glVertex3f(0.f,  1.f, 0.f);
      glTexCoord2f(1.f, 0.f); glVertex3f( 1.f,  1.f, 0.f);
      glTexCoord2f(1.f, 1.f); glVertex3f( 1.f, 0.f, 0.f);
  /*
      glTexCoord2f(0.f, 0.f); glVertex3f(-1.f, -1.f, 0.f);
      glTexCoord2f(0.f, 1.f); glVertex3f(-1.f,  1.f, 0.f);
      glTexCoord2f(1.f, 1.f); glVertex3f( 1.f,  1.f, 0.f);
      glTexCoord2f(1.f, 0.f); glVertex3f( 1.f, -1.f, 0.f);
  */
  glEnd();
  //  glBindTexture(GL_TEXTURE_2D, 0);
  glDisable(GL_TEXTURE_2D);
  //  glLoadIdentity();
}
//================================================================================================
void Graphics::draw( Vertel const&model, Vertex const&pos )const{
  glMatrixMode( GL_MODELVIEW );
  glPushMatrix();
  glLoadIdentity();
  glTranslatef( pos[0], pos[1], pos[2] ); //TODO check size
  // glColor3f(.5f,0.0,0.0);
  glBegin( GL_POLYGON );
  for( int i=0;i<4;i++){
    glVertex3fv( &(model[i][0]) );
  }
  glEnd();
  glPopMatrix();
}
//================================================================================================
void Graphics::draw( Vertel const&model, Vertex const&pos, unsigned int texid )const{
  glMatrixMode( GL_MODELVIEW );
  glPushMatrix();
  glLoadIdentity();
  //std::cout << pos[0] << pos[1] << std::endl;
  glTranslatef( pos[0], pos[1], pos[2] ); //TODO check size
  glEnable(GL_TEXTURE_2D); // #enable 2d texturing
  glBindTexture(GL_TEXTURE_2D, texid );
  glBegin( GL_POLYGON );
    for( int i=0;i<4;i++){
      glTexCoord2fv( &(texcoords[i][0]) );
      glVertex3fv( &(model[i][0]) );
    }
  glEnd();
  glDisable(GL_TEXTURE_2D);
  glPopMatrix();
}
//================================================================================================
unsigned int Graphics::select( Vertex const & point, 
			       std::vector< unsigned int > & name){

  GLuint buff[64] = {0};
  int hits;
  GLint viewport[4];

  glSelectBuffer(64,buff);
  glRenderMode( GL_SELECT );

  glMatrixMode(GL_PROJECTION);
  glPushMatrix();
  glLoadIdentity();
  
  glGetIntegerv( GL_VIEWPORT, viewport );
  gluPickMatrix(point[0],600-point[1], 1.f, 1.f, viewport );
  glOrtho(0.f, 1.f, 0.f, 1.f, 0.f, 1.f);

  glInitNames();

  std::list< DRAW_ITEM * >::iterator i;
  for(i = this->selectdraw.begin(); i!=this->selectdraw.end(); i++){
    Vertex const * pos = (*i)->pos;
    Vertel const * model = (*i)->model;

    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();

    glTranslatef( (*pos)[0], (*pos)[1], (*pos)[2] );
    
    //push the name vector on to the name stack
    for( int j = 0; j < (*i)->name.size(); j++ ) {
      glPushName( (*i)->name[j] );
    }

    glBegin( GL_POLYGON );
      for (int j=0; j<4; j++){
        glVertex3fv( &(*model)[j][0] );
    }
    glEnd();
    glPopMatrix();
    
    //pop this actor's name off the stack
    for( int j = 0; j < (*i)->name.size(); j++ ) {
      glPopName();
    }

  }
  glMatrixMode(GL_PROJECTION);
  glPopMatrix();


  glFlush();

  hits = glRenderMode( GL_RENDER );
  unsigned int ret=0;
  for(int i=0; i<hits; i++ ) {
    /*       printf( "Number:%d\n"
	    "MIN z: %d\n"
	    "MAX z: %d\n"
	    "Name on stack: %d %d\n",
	    buff[i*4],
	    buff[i*4+1],
	    buff[i*4+2],
            buff[i*4+3],
	    buff[i*4+4]
	    );// << buff[i*4] << std::endl; */
  name.resize( buff[0], 0 );
       name[0] = buff[i*4+3];
       name[1] = buff[i*4+4];
    ret = buff[i*4+3];
  }
  name.clear();
  selectdraw.clear();
  return ret;
}
//================================================================================================
