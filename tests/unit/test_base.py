#****************************************************************************
#* test_base.py
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

import os
import asyncio
import shutil
import debug_mgr.core as dmgr
import zuspec
from unittest import TestCase
from .env_config_test import EnvConfigTest


class TestBase(TestCase):

    def setUp(self) -> None:
        from zuspec.impl.ctxt import Ctxt
        tests_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.rundir = os.path.join(tests_dir, "rundir")
        self.testdir = os.path.join(self.rundir, "_".join(self.id().split('.')))

        self._dmgr = dmgr.Factory.inst().getDebugMgr()
        self._dmgr.enable(False)

        self.envcfg = EnvConfigTest()
        zuspec.EnvConfig.init(self.envcfg)

        Ctxt.inst()

        if os.path.isdir(self.testdir):
            shutil.rmtree(self.testdir)
        os.makedirs(self.testdir)

        return super().setUp()

    def tearDown(self) -> None:
#        if os.path.isdir(self.testdir):
#            shutil.rmtree(self.testdir)

        # Need to clear out cached info

        return super().tearDown()

    def addFile(self, path, content):
        print("Content:\n%s\n" % content)
        
        full_path = os.path.join(self.testdir, path)
        if os.path.dirname(path) != "":
            dirname = os.path.join(self.testdir, os.path.dirname(path))
            if not os.path.isdir(dirname):
                os.makedirs(dirname)

        with open(full_path, "w") as fp:
            fp.write(content)

#    def loadContent(self, content):
#        self.envcfg.loadContent(content)

#    def runActor(self, actor):
#        loop = asyncio.get_event_loop()
#        loop.run_until_complete(actor.run())


    def enableDebug(self, en):
        self._dmgr.enable(en)

    def justify(self, content):
        """Trim extraneous whitespace"""
        lines = content.splitlines()

        leading_trim = -1

        for i in range(len(lines)):
            line = lines[i]

            if leading_trim != -1:
                if len(line) > leading_trim:
                    lines[i] = line[leading_trim:]
                else:
                    lines[i] = ""
            else:
                line_s = line.strip()
                if line_s == "":
                    lines[i] = ""
                else:
                    leading_trim = len(line) - len(line_s)
                    lines[i] = line_s

        return "\n".join(lines)

            



