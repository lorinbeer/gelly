
#include <iostream>
//#include <Python.h>
#include <boost/python.hpp>


using namespace boost::python;

int main()
{
 
  Py_Initialize();
  //PyRun_SimpleString("from time import time,ctime\n"
  //                    "print 'Today is',ctime(time())\n");
 
  // std::cout << "hello" << std::endl;
 
  try {
    Py_Initialize();

    object main = import("__main__");
    object global(main.attr("__dict__"));
    //exec("import pygame\n" ,global,global);
    object sys = import("sys");
    //exec("import sys\nsys.path.append(\"/home/lorin/projects/ge/\")\n", global, global);
    object path = sys.attr("__dict__")["path"];
    //import("");
    path.attr("append")("/home/lorin/projects/ge/");
 
    exec_file("main.py", global, global );
      

    /*
    object main_module((
      handle<>(borrowed(PyImport_AddModule("__main__")))));

    object main_namespace = main_module.attr("__dict__");

    handle<> ignored(( PyRun_String( "print \"Hello, World\"",
                                     Py_file_input,
                                     main_namespace.ptr(),
                                     main_namespace.ptr() ) ));
    */
  } catch( error_already_set ) {
    std::cout << "Fuckup-eries" << std::endl;
    PyErr_Print();
   
  }


  return 0;
}
