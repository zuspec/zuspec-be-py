#****************************************************************************
#* task_build_task_caller.py
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
import zsp_arl_dm.core as arl_dm
from .task_caller import TaskCaller

class TaskBuildTaskCaller(object):

    def __init__(self):
        pass

    def build(self, 
              func_t : arl_dm.DataTypeFunction,
              is_solve : bool,
              func : callable):
        print("isTarget: %d" % (not is_solve))
        return TaskCaller(func, not is_solve)

