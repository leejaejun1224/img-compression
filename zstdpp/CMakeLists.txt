project(zstdpp_tests CXX)
cmake_minimum_required(VERSION 3.2)

find_package(OpenCV REQUIRED)
find_package(Threads REQUIRED)

add_executable(test_compress src/zstd.cpp)
# add_executable(test_decompress stc/test_decompress.cpp)

# target_include_directories(test_compress ${OpenCV_INCLUDE_DIRS})

set_property(TARGET test_compress PROPERTY CXX_STANDARD 14)
# set_property(TARGET test_decompress PROPERTY CXX_STANDARD 14)
target_link_libraries(test_compress ${OpenCV_LIBS} Threads::Threads zstd)
# target_link_libraries(test_decompress zstd)
