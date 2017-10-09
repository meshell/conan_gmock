from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans import CMake

# This easily allows to copy the package in other user or channel
channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "meshell")


class GMockConan(ConanFile):
    name = "gmock"
    version = "1.8.0"
    description = "Conan package for the google mock and testing framework"
    ZIP_FOLDER_NAME = "googletest-release-{}".format(version)
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "include_pdbs": [True, False],
               "cygwin_msvc": [True, False],
               "disable_pthreads": [True, False]}
    default_options = "shared=False", "include_pdbs=False", "cygwin_msvc=False", "disable_pthreads=False"
    exports = ['CMakeLists.txt', 'FindGMock.cmake']
    url = "http://github.com/meshell/conan_gmock"
    license = "https://github.com/google/googletest/blob/master/googletest/LICENSE"

    def config_options(self):
        if self.settings.compiler != "Visual Studio":
            try:  # It might have already been removed if required by more than 1 package
                del self.options.include_pdbs
            except:
                pass

    def source(self):
        zip_name = "release-{}.zip".format(self.version)
        url = "https://github.com/google/googletest/archive/{}".format(zip_name)
        download(url, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        msdos_shell = (self.settings.os == "Windows") and (self.options.cygwin_msvc == False)
        if msdos_shell:
            self.run("IF not exist _build mkdir _build")
        else:
            self.run("mkdir _build")
        flags = []
        if self.settings.compiler == "Visual Studio":
            # If msvc runtime linkage is MD or MDd, gtest_force_shared_crt should be ON. Otherwise OFF.
            vs_runtime_linkage = "ON" if self.settings.compiler.vs_runtime_linkage.find("MD") == 0 else "OFF"
            flags.append("-Dgtest_force_shared_crt={}".format(vs_runtime_linkage))
        if self.options.shared:
            flags.append("-DBUILD_SHARED_LIBS=1")
        if self.options.disable_pthreads:
            flags.append("-Dgtest_disable_pthreads=ON")
        flags.append("-DBUILD_GTEST=ON")
        # JOIN ALL FLAGS
        cxx_flags = " ".join(flags)

        cd_build = "cd _build"
        self.run('{cd} && cmake .. {cmake} {flags}'.format(cd=cd_build, cmake=cmake.command_line, flags=cxx_flags))
        self.run('{cd} && cmake --build . {config}'.format(cd=cd_build, config=cmake.build_config))

    def package(self):
        self.copy("FindGMock.cmake", dst='.', src='.')

        # Copying headers
        self.copy(pattern="*.h", dst="include", src="{}/googletest/include".format(self.ZIP_FOLDER_NAME),
                  keep_path=True)
        self.copy(pattern="*.h", dst="include", src="{}/googlemock/include".format(self.ZIP_FOLDER_NAME),
                  keep_path=True)

        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=".", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=".", keep_path=False)

        # Copying debug symbols
        if self.settings.compiler == "Visual Studio" and self.options.include_pdbs:
            self.copy(pattern="*.pdb", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['gtest', 'gtest_main', 'gmock', 'gmock_main']
        if self.settings.os == "Linux" and not self.options.disable_pthreads:
            self.cpp_info.libs.append("pthread")

        if self.options.shared:
            self.cpp_info.defines.append("GTEST_LINKED_AS_SHARED_LIBRARY=1")
