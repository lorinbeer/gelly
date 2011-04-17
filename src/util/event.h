//================================================================================================
//  Event
//
//
//
//================================================================================================
#include <SDL/SDL.h>
//================================================================================================


//================================================================================================
class Event {
public:
 Event():
  type( SDL_NOEVENT )
  {;}
  Event( SDL_EventType _type ):type( _type ){;}
  SDL_EventType gettype(){ return this->type; }
  void settype(SDL_EventType _type){ this->type = _type; }
protected:
  SDL_EventType type;
};
//================================================================================================
class MouseEvent: public Event{
public:
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
    void setkey( SDLKey _key ) {this->key = _key; }
    void setmod( SDLMod _mod ) {this->mod = _mod; }
protected:
  SDLKey key;
  SDLMod mod;
};

//================================================================================================

//================================================================================================
