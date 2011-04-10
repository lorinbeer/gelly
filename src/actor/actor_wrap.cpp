//================================================================================================
// Actor Wrapper
//  defines a boost::python wrapper for the Actor class, making it accessible to the python
//  interpreter as a python module
//
//
//================================================================================================
#include "actor.h"
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
//================================================================================================
using namespace boost::python;
//================================================================================================

//================================================================================================
//function pointers to overloaded member functions
void   (Actor::*draw1)() = &Actor::draw;
void   (Actor::*draw2)(Vertex const &) = &Actor::draw;

void   (Actor::*getpos1)(Vertex&) = &Actor::getpos;
void   (Actor::*getpos2)(float&,float&,float&) = &Actor::getpos;
Vertex*(Actor::*getpos3)() = &Actor::getpos;

void   (Actor::*setpos1)(Vertex const &) = &Actor::setpos;
void   (Actor::*setpos2)(float,float,float) = &Actor::setpos;
//================================================================================================
BOOST_PYTHON_MODULE(actor)
{
  class_< Vertex >("Vertex")
    .def(vector_indexing_suite< Vertex  >())
    ;

  class_< Actor >("Actor", init<char const *>() )
    .def( "draw", draw1 )
    .def( "draw", draw2 )
    .def( "selectdraw", &Actor::selectdraw )
    .def( "setpos", setpos1 )
    .def( "setpos", setpos2 )
    .def( "getpos", getpos1 )
    .def( "getpos", getpos2 )
    .def( "getpos", getpos3, return_value_policy< manage_new_object >() )
  ;
}
//================================================================================================
