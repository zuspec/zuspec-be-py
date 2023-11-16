#****************************************************************************
#* function_impl_trap.py
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

class FunctionImplTrap(object):

    def __init__(self, func, is_solve):
        self._func = func
        self._is_async = not is_solve
        pass

    def call(self, thread, params):
        raise Exception("Function %s not implemented" % self._func.name())

    def call_target(self, thread, params):
        raise Exception("Function %s not implemented" % self._func.name())

