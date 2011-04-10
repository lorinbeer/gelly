//================================================================================================
// SDL ENUM WRAPPER
//   wrap certain useful SDL enums for exposure in python
//
//================================================================================================

#include <SDL/SDL.h>
//#include <boost/python.hpp>
#include <boost/python/enum.hpp>
#include <boost/python/def.hpp>
#include <boost/python/module.hpp>


//================================================================================================
using namespace boost::python;
//================================================================================================
SDLKey identity_(SDLKey x) { return x; }


BOOST_PYTHON_MODULE(pysdlutil)
{
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

    .export_values()
    ;

    def("identity", identity_);
}
//================================================================================================
