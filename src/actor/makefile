#=================================================================================================
#
#
#
#=================================================================================================
#Source Code Files
SRCS = actor.cpp actor_wrap.cpp
HDRS = actor.h
#HDRS = $(SRCS:.cpp=.h)
OBJS = $(SRCS:.cpp=.o)
OUT_PATH = ../../objs
#=================================================================================================
include ../../makevar
#=================================================================================================
#add any module specific cflags and libs
INCLUDE = -I../graphics
#=================================================================================================
all: _actor.o actor_wrap.o fooactor.so
#=================================================================================================
fooactor.so: actor_wrap.o _actor.o
	g++ -shared $(ALL_LIBS) $(ALL_CFLAGS) \
	-L /home/lorin/projects/gelly \
	$(INCLUDE) \
	$(OBJS_DIR)/actor_wrap.o $(OBJS_DIR)/_actor.o \
	-o $(OUT_PATH)/fooactor.so
#=================================================================================================
_actor.o: actor.cpp actor.h
	g++ -c -fpic $(INCLUDE) \
	actor.cpp -o $(OBJS_DIR)/_actor.o 
#=================================================================================================
actor_wrap.o: actor_wrap.cpp actor.h actor.cpp
	g++ -c -fpic $(INCLUDE) $(CFLAGS) $(PYB_CFLAGS) \
	actor_wrap.cpp -o $(OBJS_DIR)/actor_wrap.o


#[~/workspace/python/Boost.Python_AddNumbersClient] > g++ -shared -L ${BOOST_ROOT}/lib -lboost_python-gcc \
#> -L ../../c++/AddNumbers/lib -lAddNumbers -o lib/AddNumbers_wrap.so obj/AddNumbers_wrap.o
#=================================================================================================
clean:
	-rm ../$(OBJS)
#=================================================================================================

