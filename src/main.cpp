//================================================================================================
#include <SDL/SDL.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <iostream>
#include <stdio.h>
#include "berkelium_util.hpp"
//================================================================================================
//#include <GL/glut.h>
//================================================================================================
#include "berkelium/Berkelium.hpp"
#include "berkelium/Window.hpp"
#include "berkelium/WindowDelegate.hpp"
#include "berkelium/Context.hpp"
//================================================================================================
#include <boost/python.hpp>
//#include <python2.6/Python.h>
//================================================================================================
#include "graphics.h"
#include "actor.h"
#include "util/event.h"
//================================================================================================
using namespace Berkelium;
using namespace boost::python;
//================================================================================================
//================================================================================================
int init_py();
object pymain;
//================================================================================================
//================================================================================================
/*  uiButtonEvent
 *   passes event data to python
 */
void uiPyEvent(std::string * message)
{
  object gbl = pymain.attr("__dict__");
  object local = exec("locals()",gbl,gbl);
  object keypress = pymain.attr("keypress");
  std::string *str = new std::string("");
  MessageEvent event(message->c_str());
  // printf("%s",str.c_str());
  try {
    object res = keypress( event );
    char * str = extract<char*>(res);
    cout << str <<"shouesthaou";
  }
  catch( error_already_set ) {
    std::cout << "Fuckup-eries" << std::endl;
    PyErr_Print();
  }

}



void bar( unsigned int actor_id )
{
  //printf( "Actor %i selected\n",actor_id );
}
//Initialize SDL
int init_ge( )
{
  Berkelium::init( FileString::empty() );
  init_py();

  return 1;
}
//================================================================================================

int init_py( )
{
  Py_Initialize();
  PyRun_SimpleString("from time import time,ctime\n" 
		     "print 'Today is',ctime(time())\n");
  try {
  pymain = import("__main__");
  object global(pymain.attr("__dict__"));

  object locals = exec("locals()", global, global);

  object sys = import("sys");
  object path = sys.attr("__dict__")["path"];

  path.attr("append")("/home/lorin/projects/gelly/src/pyge");
  path.attr("append")("/home/lorin/projects/gelly/src");
  path.attr("append")("/home/lorin/projects/gelly/objs");

  object actor_wrap = import("actor");

  exec_file("src/pyge/test.py", global, locals);

  object dungeon = import("dungeon");

  import("test");

  }
  catch( error_already_set ) {
    std::cout << "Fuckup-eries" << std::endl;
    PyErr_Print();
  }
  return 1;
}
//================================================================================================
//clean up
int clean( SDL_Surface * display )
{
  SDL_FreeSurface(display);
  SDL_Quit();
}
//================================================================================================
// Event Handling
int events( GLBerkeliumWindow * bkwindow )
{
  SDL_Event event;
  unsigned int x = 0;
  unsigned int y = 0;
  object gbl = pymain.attr("__dict__");
  object local = exec("locals()",gbl,gbl);
  object keypress = pymain.attr("keypress");
  Vertex point;
  unsigned int hit=0;
  MouseEvent *mouseevent=0;
      std::vector< unsigned int > name;

  while ( SDL_PollEvent(&event) )
  {
    switch( event.type ){
    case SDL_MOUSEMOTION:
      x = (event.button.x * 800)/800;
      y = (event.button.y * 600)/600;
      bkwindow->window()->mouseMoved(x,y);   
      break;
    case SDL_MOUSEBUTTONDOWN:
      x = (event.button.x * 800)/800;
      y = (event.button.y * 600)/600;
      bkwindow->window()->mouseMoved( x, y );
      bkwindow->window()->mouseButton( event.button.button, true);
  

      break;
    case SDL_MOUSEBUTTONUP:
      x = (event.button.x * 800)/800;
      y = (event.button.y * 600)/600; 
      bkwindow->window()->mouseMoved( x, y );
      bkwindow->window()->mouseButton( event.button.button, false);
   
      exec("drwsel()", gbl, local);
      INIT_VERTEX(point, 3);
      point[0]=x;
      point[1]=y;
      point[2]=0;
      hit = Graphics::Instance()->select(point, name );
      mouseevent = new MouseEvent( name[0], name[1], 0, 0 );
      try{

      keypress( mouseevent );
      }
      catch( error_already_set ){
        PyErr_Print();
      }
      //     bar( hit );
      break;
    case SDL_KEYDOWN:
      break;
    case SDL_KEYUP:
      try{
	//keypress( int(event.key.keysym.sym), int(event.key.keysym.mod) );
	KeyEvent elf;
        elf.settype (SDL_EventType(event.type));
        elf.setkey  (event.key.keysym.sym);
        elf.setmod  (event.key.keysym.mod);
        keypress( elf );
      }
      catch( error_already_set ) {
        std::cout << "Fuckup-eries" << std::endl;
        PyErr_Print();
      }
      break;
    case SDL_QUIT:
      return 0;
    }
  }
  return 1;
}


//================================================================================================
int main()
{
  // SDL_Surface * display = 0;
  int ticks = 0;
  Uint32 framerate = 60;
  Uint32 lastframe = 0;
  //  Uint32 startTime = SDL_GetTicks(); 
  int running = 1;
  int counter = 0;
  Graphics * gfx = Graphics::Instance();
  //  init_ge(display);
  init_ge();
  GLBerkeliumWindow * bk_texture_window = new GLBerkeliumWindow(800, 600, true);
  bk_texture_window->window()->focus();
  bk_texture_window->clear();
  bk_texture_window->uiConnectSignal( uiPyEvent );
  //bk_texture_window->loadURL( "http://www.google.com" );
  bk_texture_window->loadURL( "file:///home/lorin/projects/gelly/src/html/hud.html" );
  
  object test = import("test");
  

 
  //Actor actor;
  while (running)
  {
    
    // ticks = SDL_GetTicks() - lastframe;
    running = events(  bk_texture_window );
    //   glClearColor((128.0f / 255.0f), 1.0f, 1.0f, 1.0f); //Cyan color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    //    if( ticks >= framerate ){
 
  
  try{
    object global = pymain.attr("__dict__");
    object local = exec("locals()",global,global);
    
    exec("drw()", global, local);
  
  } 
  catch( error_already_set ) {
    std::cout << "Fuckup-eries" << std::endl;
    PyErr_Print();
  }

    Berkelium::update();
    gfx->draw( bk_texture_window->gldraw() );
    SDL_GL_SwapBuffers();
  }
      /*
      //  std::cout << counter++;
       Berkelium::update();
      lastframe = SDL_GetTicks();

      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

 
    



      bk_texture_window->loadURL( "file:///home/lorin/projects/ge1/hud1.html" );
      s = false;
    }
    else
      {
	s = true;
        
      }
    Berkelium::update();

    bk_texture_window->gldraw();

    SDL_GL_SwapBuffers();
    //   }
  }
      /*
      //  std::cout << counter++;
       Berkelium::update();
      lastframe = SDL_GetTicks();

      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

 





      glLoadIdentity();
      
      /*     glBegin(GL_QUADS);
        glColor3f(1, 0, 0); glVertex3f(0, 0, 0);
        glColor3f(1, 1, 0); glVertex3f(100, 0, 0);
        glColor3f(1, 0, 1); glVertex3f(100, 100, 0);
        glColor3f(1, 1, 1); glVertex3f(0, 100, 0);
      glEnd();
      
      bk_texture_window->draw();

            SDL_GL_SwapBuffers();
    }
  }
*/
  // clean(display);

  Py_Finalize(); 


  return 0;
}
