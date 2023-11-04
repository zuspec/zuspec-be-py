
import os
from setuptools import setup, find_namespace_packages

version="0.0.1"

if "BUILD_NUM" in os.environ.keys():
    version += "." + os.environ["BUILD_NUM"]

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
    'pytypeworks',
    'zuspec-dataclasses',
    'pyvsc-dataclasses',
    'fltools',
    'fusesoc',
    'pyyaml',
    'vsc-dm',
    'vsc-solvers',
    'zuspec-arl-dm',
    'zuspec-arl-eval',
    'zuspec-be-sw',
    'zuspec-fe-parser',
    'zuspec-parser'
  ],
)

