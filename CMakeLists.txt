project(RSSFeed)
cmake_minimum_required(VERSION 3.3)

set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} \
	-Wall \
	-Wextra \
	-pedantic")

add_executable(frss src/main.cpp)
