# Copyright 2014 Rackspace Hosting
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


GROUP = "dbaas.api.instances.metadata"

from proboscis import before_class
from proboscis import test
from proboscis.asserts import assert_equal

from trove.tests.config import CONFIG
from trove.tests.util import create_dbaas_client
from trove.tests.util.users import Requirements
from trove.common.utils import poll_until


@test(groups=[GROUP])
class MetadataTests(object):
    @before_class
    def setUp(self):
        reqs = Requirements(is_admin=False)
        self.user = CONFIG.users.find_user(reqs)
        self.dbaas = create_dbaas_client(self.user)

        self.meta_key = 'testKey'
        self.meta_value = {'one': [2, 3, 5]}
        self.new_meta_key = 'newKey'
        self.new_meta_value = {'testing': {'one': [1, 2, 3]}}

        # create an instance for running metadata tests against.
        response = self.dbaas.instances.create('metadata_test', 1,
            {'size': 1}, [])
        poll_until(lambda: self.dbaas.instances.get(response.id),
                   lambda instance: instance.status == 'RUNNING',
                   time_out=10)
        self.instance = self.dbaas.instances.get(response.id)

    def test_metadata_create(self):
        self.dbaas.metadata.create(
            self.instance.id, self.meta_key, self.meta_value)
        value = self.dbaas.metadata.show(self.instance.id, self.meta_key)
        assert_equal(value, self.meta_value,
                     'Instance metadata created successfully')
