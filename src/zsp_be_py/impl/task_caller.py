#****************************************************************************
#* task_caller.py
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
from zsp_arl_dm import ValRefToPyVal, PyValToValRef
import zsp_arl_eval.core as zsp_eval
from .deferred_task_caller import DeferredTaskCaller
from .runner_thread import RunnerThread

class TaskCaller(object):

    def __init__(self, 
                 ctxt,
                 func,
                 is_async):
        self._func = func
        self._is_async = is_async
        self._ctxt = ctxt
        self._param_xformers = []
        self._ret_xformer = None
        pass

    def call(self, thread, params):
        func_params = []
        for i,p in enumerate(params):
            func_params.append(ValRefToPyVal().toPyVal(p))

        ret = self._func(*func_params)

        if ret is None:
            thread.setResult(thread.mkValRefInt(0, False, 1))
        else:
            thread.setResult(PyValToValRef(self._ctxt).toValRef(ret))

    async def call_target(self, thread, params):
        func_params = []
        for p in params:
            func_params.append(ValRefToPyVal(thread).toPyVal(p))

        ret = await self._func(*func_params)

        if ret is None:
            thread.setResult(thread.mkValRefInt(0, False, 1))
        else:
            thread.setResult(PyValToValRef(self._ctxt).toValRef(ret))
