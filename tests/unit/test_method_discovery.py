#****************************************************************************
#* test_method_discovery.py
#*
#* Copyright 2022 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************
from .test_base import TestBase
import inspect

def find_method(frame, name):
    ret = None

    if name in frame.f_locals.keys():
        print("Found method %s in locals" % name)
        ret = frame.f_locals[name]

    if ret is None and "self" in frame.f_locals.keys():
        self = frame.f_locals["self"]
        ret = getattr(self, name, None)
    
    if ret is None and name in frame.f_globals.keys():
        print("Found method %s in globals" % name)
        ret = frame.f_globals[name]

    return ret

def glbl_method():
    pass

class TestMethodDiscovery(TestBase):

    def cls_method(self):
        pass


    def test_find_inner_method(self):

        def my_method(a, b, c):
            pass

        self.assertIsNotNone(find_method(inspect.currentframe(), "my_method"))

    def test_find_cls_method(self):

        self.assertIsNotNone(find_method(inspect.currentframe(), "cls_method"))

    def test_find_glbl_method(self):

        self.assertIsNotNone(find_method(inspect.currentframe(), "glbl_method"))



