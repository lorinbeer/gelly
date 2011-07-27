//================================================================================================
//  Event
//
//
//
//================================================================================================
#include <SDL/SDL.h>
#include <boost/algorithm/string.hpp>
#include <string>
#include <vector>
//================================================================================================
using namespace std;
using namespace boost;
//================================================================================================
class Event {
public:
 Event():
  type( SDL_NOEVENT )
  {;}
  Event( int _type ):type( _type ){;}
  int gettype(){ return this->type; }
  void settype(int _type){ this->type = _type; }
protected:
  int type;
};
//================================================================================================
class MouseEvent: public Event{
public:
  MouseEvent():
    Event( SDL_MOUSEBUTTONUP ),
    x(0),
    y(0),
    button(0),
    state(0){;}

  MouseEvent( unsigned int _x,
	     unsigned int _y,
	     unsigned int _button,
             unsigned int _state ):
    Event( SDL_MOUSEBUTTONUP),
    x(0),
    y(0),
    button(0),
    state(0)
  {
    x = _x;
    y = _y;
    button = _button;
    state  = _state;
  }

  unsigned int getx     () { return this->x; }
  unsigned int gety     () { return this->y; }
  unsigned int getbutton() { return this->button; }
  unsigned int getstate () { return this->state; }
  void setx     ( unsigned int _x      ) { this->x      = _x; } 
  void sety     ( unsigned int _y      ) { this->x      = _y; } 
  void setbutton( unsigned int _button ) { this->button = _button; }
  void setstate ( unsigned int _state  ) { this->state  = _state; }
protected:
  unsigned int x,y;
  unsigned int button;
  unsigned int state;
};
//================================================================================================
class KeyEvent: public Event{
public:
    SDLKey getkey() { return this->key; }
    SDLMod getmod() { return this->mod; }
    void setkey( SDLKey _key ) {this->key = _key;}
    void setmod( SDLMod _mod ) {this->mod = _mod;}
protected:
  SDLKey key;
  SDLMod mod;
};
//================================================================================================
class MessageEvent {
public:
  MessageEvent():
    type((int)SDL_SYSWMEVENT+1),
    target(0),
    action(0),
    message(0)    
    {;}
  MessageEvent(string _msg):
    type((int)SDL_SYSWMEVENT+1),
    target(0),
    action(0),
    message(0){
      string args;
      vector< string > strsplit;
      vector< string > subsplit;
      split( strsplit, _msg, is_any_of(";"), token_compress_on );
      switch(strsplit.size()) {
      case 3: //function call and arguments
        this->message = this->setstr( strsplit[2] );
      case 2: //function without arguments
        split( subsplit, strsplit[0], is_any_of("="), token_compress_on );
        if( subsplit.size() == 2 ) {
          if( subsplit[0].compare("target") == 0 ){
            this->target = this->setstr( subsplit[1] );
	  }
          else {}
          subsplit.clear();
          split( subsplit, strsplit[1], is_any_of("="), token_compress_on );
          if( subsplit[0].compare("request") == 0 ){
            this->action = this->setstr( subsplit[1] );
	  }
          else{}
	 }
        break;
      default: //any other case
        printf("js message error/n");
      }
    }
  int gettype() {return this->type;}
  const char * getmsg() {return this->message;}
  const char * gettrg() {return this->target;}
  const char * getact() {return this->action;}
  void settype(int _type) {this->type=_type;}
  void setmsg(const char * _msg) {;}
  void settrg(const char * _msg) {;}
  void setact(const char * _msg) {;}
protected:
  //================================================================================================
  char* setstr(string & str){
    char * dest = new char[ (int)(str.length()+1) ];
    for(int i=0;i<str.length();i++){
      dest[i] = str[i];
    } 
   dest[str.length()] = '\0';
   return dest;
  } 
  //================================================================================================
  int type;
  char * target;
  char * action;
  char * message;
};
//================================================================================================
