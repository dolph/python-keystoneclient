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


class Endpoint(base.Resource):
    """Represents an Identity endpoint.

    Attributes:
        * id: a uuid that identifies the endpoint

    """
    pass


class EndpointManager(base.CrudManager):
    """Manager class for manipulating Identity endpoints."""
    resource_class = Endpoint
    collection_key = 'endpoints'
    key = 'endpoint'

    def create(self, service, url, name=None, interface=None, region=None):
        return super(EndpointManager, self).create(
            service_id=base.getid(service),
            name=name,
            interface=interface,
            url=url,
            region=region)

    def get(self, endpoint):
        return super(EndpointManager, self).get(
            endpoint_id=base.getid(endpoint))

    def update(self, endpoint, service=None, url=None, name=None,
               interface=None, region=None):
        return super(EndpointManager, self).update(
            endpoint_id=base.getid(endpoint),
            service_id=base.getid(service),
            name=name,
            interface=interface,
            url=url,
            region=region)

    def delete(self, endpoint):
        return super(EndpointManager, self).delete(
            endpoint_id=base.getid(endpoint))
