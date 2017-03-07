[![Build Status](https://travis-ci.org/meshell/conan_gmock.svg)](https://travis-ci.org/meshell/conan_gmock)
[![Build status](https://ci.appveyor.com/api/projects/status/ia1g9wue32t0pswa?svg=true)](https://ci.appveyor.com/project/meshell/conan-gmock)
[![Conan.io](https://img.shields.io/badge/conan.io-gmock%2F1.8.0-green.svg)](http://www.conan.io/source/gmock/1.8.0/meshell/stable)


# conan_gmock

[Conan.io](https://conan.io) package for Google test and mocking library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/gmock/1.8.0/meshell/stable).

## Credits

This project is a modified version of [conan-gtest](https://github.com/lasote/conan-gtest) by [lasote](https://github.com/lasote)

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

## Upload packages to server

    $ conan upload gmock/1.8.0@meshell/stable --all

## Reuse the packages

### Basic setup

    $ conan install gmock/1.8.0@meshell/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    gmock/1.8.0@meshell/stable

    [options]
    gmock:shared=true # false
    gmock:include_pdbs=false # MSVC - include debug symbols
    gmock:disable_pthreads=false # set to true for MinGW under Windows

    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install .

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
