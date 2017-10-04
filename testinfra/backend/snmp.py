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

from testinfra.backend import base


class SnmpBackend(base.BaseBackend):
    """Run SNMP command"""
    NAME = "snmp"

    def __init__(self, host, *args, **kwargs):
        self.host = host
        super(SnmpBackend, self).__init__(self.host, *args, **kwargs)

    def run(self, command, *args, **kwargs):

        if command not in ['snmpget', 'snmpwalk']:
            raise ValueError('command must be either snmpget or snmpwalk')

        oid = kwargs.get('oid')
        if not oid:
            raise ValueError('oid missing')

        return self.run_snmp(self.get_command(command), oid, *args, **kwargs)

    def run_snmp(self, command, oid, version='2c', community='public',
                 *args, **kwargs):

        cmd = [command]
        cmd.append('-Oe -Ob -Oq -Ot -OU')

        if version == '2c':
            cmd.append("-v 2c")
            cmd.append("-c")
            cmd.append(community)

        cmd.append(self.host)
        cmd.append(oid)

        out = self.run_local(" ".join(cmd))
        out.command = self.encode(command)
        return out
