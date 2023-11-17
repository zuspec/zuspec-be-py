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
from .env_config_cocotb import EnvConfigCocotb

class EnvConfig(object):

    _inst = None
    _provider_f = [
        EnvConfigCocotb
    ]

    def __init__(self, provider):
        self._provider = provider
        pass

    def getRunnerBackend(self):
        return self._provider.getRunnerBackend()
    
    def getContext(self) -> 'Context':
        return self._provider.getContext()
    
    @classmethod
    def addProviderFactory(cls, f, insert=True):
        if f not in cls._provider_f:
            if insert:
                cls._provider_f.insert(0, f)
            else:
                cls._provider_f.append(f)

    @classmethod
    def inst(cls):
        # if cls._inst is None:
        #     raise Exception("EnvConfig has not been set")
            # provider = None
            # for f in cls._provider_f:
            #     provider = f.create()
            #     if provider is not None:
            #         break
            
            # if provider is None:
            #     raise Exception("Failed to auto-detect environment")
            # cls._inst = EnvConfig(provider)
        return cls._inst

    @classmethod
    def init(cls, provider):
        cls._inst = EnvConfig(provider)


