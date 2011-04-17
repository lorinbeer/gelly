//================================================================================================
// SDL ENUM WRAPPER
//   wrap certain useful SDL enums for exposure in python
//
//================================================================================================

#include <SDL/SDL.h>
#include <boost/python.hpp>
//================================================================================================
#include "event.h"
//================================================================================================
using namespace boost::python;
//================================================================================================
SDLKey identify(SDLKey x) { return x; }


BOOST_PYTHON_MODULE(pysdlutil)
{


  class_< Event >("Event")
    .add_property("type", &Event::gettype, &Event::settype)
    ;
  class_< MouseEvent >("MouseEvent")
    .add_property("type", &MouseEvent::gettype, &MouseEvent::settype)
    .add_property("x", &MouseEvent::getx, &MouseEvent::setx)
    .add_property("y", &MouseEvent::gety, &MouseEvent::sety)
    .add_property("button", &MouseEvent::getbutton, &MouseEvent::setbutton)
    .add_property("state", &MouseEvent::getstate, &MouseEvent::setstate)
    ;
  class_< KeyEvent >("KeyEvent")
    .add_property("type", &KeyEvent::gettype, &KeyEvent::settype)
    .add_property("key", &KeyEvent::getkey, &KeyEvent::setkey)
    .add_property("mod", &KeyEvent::getmod, &KeyEvent::setmod)
    ;
  //==============================================================================================
  enum_< SDLKey >("SDLKey")
    //numeric
    .value("SDLK_0", SDLK_0) //0
    .value("SDLK_1", SDLK_1) //1
    .value("SDLK_2", SDLK_2) //2
    .value("SDLK_3", SDLK_3) //3
    .value("SDLK_4", SDLK_4) //4
    .value("SDLK_5", SDLK_5) //5
    .value("SDLK_6", SDLK_6) //6
    .value("SDLK_7", SDLK_7) //7
    .value("SDLK_8", SDLK_8) //8
    .value("SDLK_9", SDLK_9) //9
    //keypad numeric
    .value("SDLK_KP0", SDLK_0) //0
    .value("SDLK_KP1", SDLK_1) //1
    .value("SDLK_KP2", SDLK_2) //2
    .value("SDLK_KP3", SDLK_3) //3
    .value("SDLK_KP4", SDLK_4) //4
    .value("SDLK_KP5", SDLK_5) //5
    .value("SDLK_KP6", SDLK_6) //6
    .value("SDLK_KP7", SDLK_7) //7
    .value("SDLK_KP8", SDLK_8) //8
    .value("SDLK_KP9", SDLK_9) //9
    //arrow keys
    .value("SDLK_UP"   , SDLK_UP   ) //up arrow
    .value("SDLK_DOWN" , SDLK_DOWN ) //down arrow
    .value("SDLK_RIGHT", SDLK_RIGHT) //right arrow
    .value("SDLK_LEFT" , SDLK_LEFT ) //left arrow
    //special
    .value("SDLK_SPACE", SDLK_SPACE ) //space bar
    .value("SDLK_RETURN", SDLK_RETURN ) //return
    .value("SDLK_PAUSE", SDLK_PAUSE ) //pause
    .value("SDLK_ESCAPE", SDLK_ESCAPE ) //escape key
    .value("SDLK_BACKSPACE", SDLK_BACKSPACE ) //backspace
    .value("SDLK_TAB", SDLK_TAB ) //tab
    .value("SDLK_CLEAR", SDLK_CLEAR ) //clear
    //alphabetic keys
    .value("SDLK_a", SDLK_a )//a
    .value("SDLK_b", SDLK_b )//b
    .value("SDLK_c", SDLK_c )//c
    .value("SDLK_d", SDLK_d )//d
    .value("SDLK_e", SDLK_e )//e
    .value("SDLK_f", SDLK_f )//f
    .value("SDLK_g", SDLK_g )//g
    .value("SDLK_h", SDLK_h )//h
    .value("SDLK_i", SDLK_i )//i
    .value("SDLK_j", SDLK_j )//j
    .value("SDLK_k", SDLK_k )//k
    .value("SDLK_l", SDLK_l )//l
    .value("SDLK_m", SDLK_m )//m
    .value("SDLK_n", SDLK_n )//n
    .value("SDLK_o", SDLK_o )//o
    .value("SDLK_p", SDLK_p )//p
    .value("SDLK_q", SDLK_q )//q
    .value("SDLK_r", SDLK_r )//r
    .value("SDLK_s", SDLK_s )//s
    .value("SDLK_t", SDLK_t )//t
    .value("SDLK_u", SDLK_u )//u
    .value("SDLK_v", SDLK_v )//v
    .value("SDLK_w", SDLK_w )//w
    .value("SDLK_x", SDLK_x )//x
    .value("SDLK_y", SDLK_y )//y
    .value("SDLK_z", SDLK_z )//z
    //key mods

    //function keys
    .value("SDLK_F1" , SDLK_F1  ) // F1
    .value("SDLK_F2" , SDLK_F2  ) // F2
    .value("SDLK_F3" , SDLK_F3  ) // F3
    .value("SDLK_F4" , SDLK_F4  ) // F4
    .value("SDLK_F5" , SDLK_F5  ) // F5
    .value("SDLK_F6" , SDLK_F6  ) // F6
    .value("SDLK_F7" , SDLK_F7  ) // F7
    .value("SDLK_F8" , SDLK_F8  ) // F8
    .value("SDLK_F9" , SDLK_F9  ) // F9
    .value("SDLK_F10", SDLK_F10 ) // F10
    .value("SDLK_F11", SDLK_F11 ) // F11
    .value("SDLK_F12", SDLK_F12 ) // F12
    .value("SDLK_F13", SDLK_F13 ) // F13
    .value("SDLK_F14", SDLK_F14 ) // F14
    .value("SDLK_F15", SDLK_F15 ) // F15


    .export_values()
    ;
  //==============================================================================================

  //==============================================================================================
  enum_< SDL_EventType >("SDL_EventType")
    .value("NOEVENT"        , SDL_NOEVENT)        //used for initialization 
    //    .value("WINDOWEVENT"    , SDL_WINDOWEVENT)    //window state change
    .value("KEYDOWN"        , SDL_KEYDOWN)        //keys pressed
    .value("KEYUP"          , SDL_KEYUP)          //keys released
    //    .value("TEXTINPUT"      , SDL_TEXTINPUT)      //keyboard text input
    .value("MOUSEMOTION"    , SDL_MOUSEMOTION)    //mouse moved
    .value("MOUSEBUTTONDOWN", SDL_MOUSEBUTTONDOWN)//mouse button pressed
    .value("MOUSEBUTTONUP"  , SDL_MOUSEBUTTONUP)  //mouse button released
    //    .value("MOUSEWHEEL"     , SDL_MOUSEWHEEL)     //mouse wheel motion
    .value("JOYAXISMOTION"  , SDL_JOYAXISMOTION)  //joystick axis motion
    .value("JOYBALLMOTION"  , SDL_JOYBALLMOTION)  //joystick trackball motion
    .value("JOYHATMOTION"   , SDL_JOYHATMOTION)   //joystick hat position change
    .value("JOYBUTTONDOWN"  , SDL_JOYBUTTONDOWN)  //joystick button pressed
    .value("JOYBUTTONUP"    , SDL_JOYBUTTONUP)    //joystick button released
    .value("QUIT"           , SDL_QUIT)           //user-requested quit
    .value("SYSWMEVENT"     , SDL_SYSWMEVENT)     //system specific event
    //    .value("PROXIMITYIN"    , SDL_PROXIMITYIN)    //proximity In event
    //    .value("PROXIMITYOUT"   , SDL_PROXIMITYOUT)   //proximity Out event
    //    .value("EVENT_RESERVED1", SDL_EVENT_RESERVED1)//Reserved for future use

    .export_values()
    ;
  //==============================================================================================
  //==============================================================================================

  //==============================================================================================
}
//================================================================================================
//remaining keys to implement
/*



SDLK_EXCLAIM	'!'	exclaim
SDLK_QUOTEDBL	''	quotedbl
SDLK_HASH	'#'	hash
SDLK_DOLLAR	'$'	dollar
SDLK_AMPERSAND	'&'	ampersand
SDLK_QUOTE	'''	quote
SDLK_LEFTPAREN	'('	left parenthesis
SDLK_RIGHTPAREN	')'	right parenthesis
SDLK_ASTERISK	'*'	asterisk
SDLK_PLUS	'+'	plus sign
SDLK_COMMA	','	comma
SDLK_MINUS	'-'	minus sign
SDLK_PERIOD	'.'	period
SDLK_SLASH	'/'	forward slash

SDLK_COLON	':'	colon
SDLK_SEMICOLON	';'	semicolon
SDLK_LESS	'<'	less-than sign
SDLK_EQUALS	'='	equals sign
SDLK_GREATER	'>'	greater-than sign
SDLK_QUESTION	'?'	question mark
SDLK_AT	'@'	at
SDLK_LEFTBRACKET	'['	left bracket
SDLK_BACKSLASH	'\'	backslash
SDLK_RIGHTBRACKET	']'	right bracket
SDLK_CARET	'^'	caret
SDLK_UNDERSCORE	'_'	underscore
SDLK_BACKQUOTE	'`'	grave

SDLK_DELETE	'^?'	delete

SDLK_KP_PERIOD	'.'	keypad period
SDLK_KP_DIVIDE	'/'	keypad divide
SDLK_KP_MULTIPLY	'*'	keypad multiply
SDLK_KP_MINUS	'-'	keypad minus
SDLK_KP_PLUS	'+'	keypad plus
SDLK_KP_ENTER	'\r'	keypad enter
SDLK_KP_EQUALS	'='	keypad equals
SDLK_UP	 	up arrow
SDLK_DOWN	 	down arrow
SDLK_RIGHT	 	right arrow
SDLK_LEFT	 	left arrow
SDLK_INSERT	 	insert
SDLK_HOME	 	home
SDLK_END	 	end
SDLK_PAGEUP	 	page up
SDLK_PAGEDOWN	 	page down

SDLK_NUMLOCK	 	numlock
SDLK_CAPSLOCK	 	capslock
SDLK_SCROLLOCK	 	scrollock
SDLK_RSHIFT	 	right shift
SDLK_LSHIFT	 	left shift
SDLK_RCTRL	 	right ctrl
SDLK_LCTRL	 	left ctrl
SDLK_RALT	 	right alt
SDLK_LALT	 	left alt
SDLK_RMETA	 	right meta
SDLK_LMETA	 	left meta
SDLK_LSUPER	 	left windows key
SDLK_RSUPER	 	right windows key
SDLK_MODE	 	mode shift
SDLK_HELP	 	help
SDLK_PRINT	 	print-screen
SDLK_SYSREQ	 	SysRq
SDLK_BREAK	 	break
SDLK_MENU	 	menu
SDLK_POWER	 	power
SDLK_EURO	 	euro

*/
