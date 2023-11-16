#****************************************************************************
#* test_reg_model.py
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

class TestRegModel(TestBase):

    def test_read32(self):
        content = """
        import addr_reg_pkg::*;

        component my_regs : reg_group_c {
            reg_c<bit[32]>      r1;
            reg_c<bit[32]>      r2;
        }

        component pss_top {
            my_regs     regs;
            action Entry { 
                exec body {
                    comp.regs.r1.read();
                }
            }
        }
        """

        doit_called = 0

        def read32(addr : int) -> int:
            print("read32")
            pass

        self.enableDebug(True)

        self.loadContent(content)

        actor = zuspec.Actor("pss_top", "pss_top::Entry")
        self.runActor(actor)

        self.assertEqual(doit_called, 1)
