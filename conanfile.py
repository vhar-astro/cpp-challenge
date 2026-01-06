from pathlib import Path

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout


def _read_version():
    return Path(__file__).parent.joinpath("VERSION").read_text().strip()


class MyLibRecipe(ConanFile):
    name = "mylib"
    version = _read_version()
    package_type = "library"
    license = "MIT"
    url = "https://github.com/example/mylib"
    description = "Trivial sum library for CI/CD demonstration"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    exports_sources = (
        "CMakeLists.txt",
        "cmake/*",
        "include/*",
        "src/*",
        "tests/*",
        "VERSION",
        "LICENSE",
    )
    requires = "gtest/1.14.0"

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["CMAKE_POSITION_INDEPENDENT_CODE"] = True
        tc.cache_variables["MYLIB_BUILD_TESTS"] = False
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["mylib"]
