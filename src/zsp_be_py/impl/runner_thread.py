#****************************************************************************
#* runner_thread.py
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

from .runner_backend import RunnerBackend

class RunnerThread(object):

    def __init__(self, backend : RunnerBackend):
        self.backend = backend
        self.changed = backend.mkEvent()
        self.event = backend.mkEvent()
        self.queue = []

        self.run_task = self.backend.start(self.run())
        pass

    def queue_call(self, caller):
        print("-- queue_call")
        self.queue.append(caller)
        self.event.set()

    async def run(self):
        while True:
            while len(self.queue) == 0:
                await self.event.wait()
            self.event.clear()

            caller = self.queue.pop(0)

            print("caller: %s" % str(caller))

            if caller is None:
                # We've been requested to halt
                break
            else:
                await caller.call()
                self.changed.set()


