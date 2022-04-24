from distutils.core import setup, Extension

module = Extension("gommoku", sources=["functions.c"], extra_compile_args=["-Wall"])


def main():
    setup(name="gommoku",
          version="1.0.0",
          description="gommoku solver",
          author="nic",
          author_email="nicolas.jan.stas@gmail.com",
          ext_modules=[module])

if __name__ == "__main__":
    main()