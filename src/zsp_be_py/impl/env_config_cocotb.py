#****************************************************************************
#* env_config.py
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
import sys

class EnvConfigCocotb(object):

    def __init__(self, backend):
        self._backend = backend
        self._ctxt = None

    def getContext(self):
        if self._ctxt is None:
            pass
        return self._ctxt
        pass

    def getRunnerBackend(self):
        return self._backend

    @classmethod
    def create(cls):
        if "cocotb" in sys.modules.keys():
            from .runner_backend_cocotb import RunnerBackendCocotb
            return EnvConfigCocotb(RunnerBackendCocotb())
        else:
            return None


