cmake_minimum_required(VERSION 3.31)
project(wCoreMain)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
include(FetchContent)

add_compile_options(-fdiagnostics-color=always)
if(CMAKE_COLOR_DIAGNOSTICS)
    set(CMAKE_COLOR_DIAGNOSTICS ON)
endif()


find_package(fmt REQUIRED)
find_package(Threads REQUIRED)
find_package(replxx REQUIRED)
find_package(SQLiteCpp REQUIRED) 

add_library(wCore windows/wCore.c)
add_library(query SHARED query.cpp)
target_link_libraries(query PRIVATE SQLiteCpp)

set(libs
    wCore
    fmt::fmt
    replxx::replxx
    Threads::Threads

)
add_custom_command(TARGET query POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E echo "Copying $<TARGET_FILE:query> to ${CMAKE_SOURCE_DIR}/src/core/"
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:query> ${CMAKE_SOURCE_DIR}/src/core/
    VERBATIM
)

