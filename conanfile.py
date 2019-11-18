from conans import ConanFile, CMake, tools


class MinizipConan(ConanFile):
    name = "minizip"
    version = "2.9.1"
    license = "zlib"
    author = "Nathan Moinvaziri"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "minizip is a zip manipulation library written in C that is supported on Windows, macOS, and Linux."
    topics = ("zip", "encryption", "compression")
    settings = "os", "compiler", "build_type", "arch"
    requires = "zlib/1.2.8"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/nmoinvaz/minizip.git --branch 2.9.1")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("minizip/CMakeLists.txt", "project(minizip)",
                              '''PROJECT(minizip)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="minizip")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/. %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src=".")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["minizip"]

