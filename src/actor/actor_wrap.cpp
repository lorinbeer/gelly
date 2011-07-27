//================================================================================================
// Actor Wrapper
//  defines a boost::python wrapper for the Actor class, making it accessible to the python
//  interpreter as a python module
//
//
//================================================================================================
#include "actor.h"
#include "animactor.h"
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <vector>
#include <list>
#include <string>
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


//void   (Animactor::*animdraw1)() = &Animactor::draw;

//================================================================================================
void pysetvertel( Vertel & self, list & vertexlist ) {
  stl_input_iterator< tuple > i(vertexlist), end;
  while ( i != end ){
    stl_input_iterator< float > t(*i), subend;
    Vertex point;
    while (t != subend ){
      point.push_back(*t);
      t++;
    }
    self.push_back(point);
    i++;

  }
}
//================================================================================================
//Python Animated Actor Class
// acts as an interface between the C++ Animactor class, and a python client
// extracts c-types from python arguments for use with Animactor
class PyAnimactor
{
  public:
  PyAnimactor( list & frames, Vertel & _model ):
    wanimactor(0)
  {
    //
    std::vector< std::string > cframes;
    stl_input_iterator< std::string > begin(frames), end;
    while ( begin != end ){
      cframes.push_back( (*begin) );
      //     printf( "%s\n", (*begin).c_str() );
      begin++;
    }
    wanimactor = new Animactor( cframes, _model );
  }
  void draw( Vertex const & npos ){
    this->wanimactor->draw( npos );
  }

  //GET&SET for currentframe
  int getcurrentframe(){ return this->wanimactor->currentframe; }
  void setcurrentframe(int frame){ this->wanimactor->currentframe = frame; }
  bool getdone(){ return this->wanimactor->done; }
  void setdone( bool nstate ) { this->wanimactor->done = nstate; }


  private:
    Animactor * wanimactor;
}; 

//================================================================================================
BOOST_PYTHON_MODULE(actor)
{
  class_< std::vector< int > >("IntVec")
    .def(vector_indexing_suite< std::vector< int > >() )
    ;
  class_< std::vector< std::string > >("StrVec")
    .def(vector_indexing_suite< std::vector< std::string > >() )
    ;
  class_< Vertex >("Vertex")
    .def(vector_indexing_suite< Vertex  >())
  ;
  class_< Vertel >("Vertel")
    .def(vector_indexing_suite< Vertel >())
    .def( "set", pysetvertel )
  ;

  class_< Actor >("Actor", init<char const *,const Vertel &, const Vertel &>() )
    //.def( init<>() 
    .def( "draw", draw1 )
    .def( "draw", draw2 )
    .def( "selectdraw", &Actor::selectdraw )
    .def( "setpos", setpos1 )
    .def( "setpos", setpos2 )
    .def( "getpos", getpos1 )
    .def( "getpos", getpos2 )
    .def( "getpos", getpos3, return_value_policy< manage_new_object >() )
  ;

  class_<PyAnimactor>("Animactor", init<list&,Vertel&>() )
    // .def( "update", &Animactor::update )
    .add_property( "done", &PyAnimactor::getdone, &PyAnimactor::setdone )
    .add_property( "currentframe", &PyAnimactor::getcurrentframe, &PyAnimactor::setcurrentframe )
    .def( "draw", &PyAnimactor::draw )
  ;
}
//================================================================================================
