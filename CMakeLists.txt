# Specify the minimum version of CMake required
cmake_minimum_required(VERSION 3.20)

# Set the name of the project
project(VitvDocsLauncher C)

# Specify the C++ standard
set(CMAKE_C_STANDARD 17)


#Paths
set (APP_PATH "src/launcher")

# Add executable target and its source files
include_directories(${APP_PATH}/include)
add_executable(vitvdocslauncher ${APP_PATH}/src/launcher.c ${APP_PATH}/src/vitvlog.c)

#install
install (TARGETS vitvdocslauncher DESTINATION .)
