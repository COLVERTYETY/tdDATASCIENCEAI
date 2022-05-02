from distutils.core import setup, Extension

module = Extension("gommoku", sources=["functions.cpp"], extra_compile_args=["-Wall","-O3","-fno-stack-protector","-march=native","-fPIC","-fopenmp"])


def main():
    setup(name="gommoku",
          version="1.0.0",
          description="gommoku solver",
          author="nic",
          author_email="nicolas.jan.stas@gmail.com",
          ext_modules=[module])

if __name__ == "__main__":
    main()