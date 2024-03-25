
import os
import sys
from setuptools import setup, find_namespace_packages

version="0.0.1"

proj_dir = os.path.dirname(os.path.abspath(__file__))
try:
    sys.path.insert(0, os.path.join(proj_dir, "src/zsp_be_py"))
    from __build_num__ import BUILD_NUM
    version += ".%s" % str(BUILD_NUM)
except ImportError as e:
    print("No build_num: %s" % str(e))

setup(
  name = "zuspec-be-py",
  version=version,
  packages=find_namespace_packages(where='src'),
  package_dir = {'' : 'src'},
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = "Co-specification of hardware, software, design, and test behavior",
  long_description="""
  Co-specification of hardware, software, design, and test behavior
  """,
  license = "Apache 2.0",
  keywords = ["PSS", "Functional Verification", "RTL", "Verilog", "SystemVerilog"],
  url = "https://github.com/zuspec/zuspec-be-py",
#  entry_points={
#    'console_scripts': [
#      'zuspec = zuspec.__main__:main'
#    ]
#  },
  setup_requires=[
    'setuptools_scm',
  ],
  install_requires=[
    'zuspec-arl-dm',
    'zuspec-arl-eval',
    'zuspec-fe-parser',
    'zuspec-parser'
  ],
)

