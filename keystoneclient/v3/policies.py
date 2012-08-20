# Copyright 2011 OpenStack LLC.
# Copyright 2011 Nebula, Inc.
# All Rights Reserved.
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

from keystoneclient import base


class Policy(base.Resource):
    """Represents an Identity policy.

    Attributes:
        * id: a uuid that identifies the policy
        * endpoint_id: references the endpoint the policy applies to
        * blob: a policy document (blob)
        * type: the mime type of the policy blob

    """
    def update(self, endpoint=None, blob=None, type=None):
        kwargs = {
            'endpoint_id': (base.getid(endpoint)
                            if endpoint is not None
                            else self.endpoint_id),
            'blob': blob if blob is not None else self.blob,
            'type': type if type is not None else self.type,
        }

        try:
            retval = self.manager.update(self.id, **kwargs)
            self = retval
        except Exception:
            retval = None

        return retval


class PolicyManager(base.CrudManager):
    """Manager class for manipulating Identity policies."""
    resource_class = Policy
    collection_key = 'policies'
    key = 'policy'

    def create(self, endpoint, blob, type='application/json'):
        return super(PolicyManager, self).create(
            endpoint_id=base.getid(endpoint),
            blob=blob,
            type=type)

    def get(self, policy):
        return super(PolicyManager, self).get(
            policy_id=base.getid(policy))

    def list(self, endpoint=None):
        return super(PolicyManager, self).list(
            endpoint_id=base.getid(endpoint))

    def update(self, entity, endpoint=None, blob=None, type=None):
        return super(PolicyManager, self).update(
            policy_id=base.getid(entity),
            endpoint_id=base.getid(endpoint),
            blob=blob,
            type=type)

    def delete(self, policy):
        return super(PolicyManager, self).delete(
            policy_id=base.getid(policy))
