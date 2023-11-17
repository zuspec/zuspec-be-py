#****************************************************************************
#* actor.py
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
from .impl.env_config import EnvConfig
from .impl.runner import Runner

class Actor(object):

    def __init__(self, comp_t, action_t):
        self._comp_t = comp_t
        self._action_t = action_t

    async def run(self):
        # Get the active configuration, probing the
        # environment if necessary
        envcfg = EnvConfig.inst()

        runner = Runner(
            self._comp_t,
            None,
            ctxt=envcfg.getContext(),
            backend=envcfg.getRunnerBackend())

        await runner.run(self._action_t)
