# coding: utf-8
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import unicode_literals

from testinfra.modules.base import Module


class SNMP(Module):

    def __init__(self, community='public', version='2c'):
        self.community = community
        self.version = version

    def walk(self, oid):
        output = self.check_output('snmpwalk', oid, community=self.community,
                                   version=self.version)

        return [tuple(i.split()) for i in output.split('\n')]

    def get(self, oid):
        if not oid.endswith('.0'):
            oid += '.0'
        output = self.check_output('snmpget', oid, community=self.community,
                                   version=self.version)

        return tuple(output.split())
