from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourcefiles = ['testcy_bind.pyx']
ext_modules = [Extension(
    "cy_bind",  
    sourcefiles
)]

setup(
  name = 'Cython Bind Test',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)