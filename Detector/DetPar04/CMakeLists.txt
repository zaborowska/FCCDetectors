################################################################################
#Package : DetPar04
################################################################################

install(DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/compact DESTINATION ${CMAKE_INSTALL_DATADIR}/${CMAKE_PROJECT_NAME}/Detector/DetPar04)

file(GLOB sources src/*.cpp)
add_dd4hep_plugin(DetPar04 SHARED ${sources})
target_link_libraries(DetPar04 DD4hep::DDCore)
