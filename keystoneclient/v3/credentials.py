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


class Credential(base.Resource):
    """Represents an Identity credential.

    Attributes:
        * id: a uuid that identifies the credential

    """
    pass


class CredentialManager(base.CrudManager):
    """Manager class for manipulating Identity credentials."""
    resource_class = Credential
    key = 'credential'
    collection_key = 'credentials'
