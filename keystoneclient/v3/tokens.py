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


class Token(base.Resource):
    """Represents an Identity token.

    Attributes:
        * id: a uuid that identifies the token
        * expires
        * users
        * project
        * catalog
        * url

    """

    def revoke(self):
        return self.manager.delete(self)


class TokenManager(base.CrudManager):
    """Manager class for manipulating Identity tokens."""
    resource_class = Token
    collection_key = 'tokens'
    key = 'token'

    def authenticate(self, user=None, token=None, user_name=None,
            password=None, tenant=None, tenant_name=None):
        user_id = base.getid(user)
        token_id = base.getid(token)
        tenant_id = base.getid(tenant)

        body = {'auth': {}}

        if token_id is not None:
            body['auth']['token_id']
        elif user_id is not None or user_name is not None:
            body['auth']['passwordCredentials'] = {}

            if user_id is not None:
                body['auth']['passwordCredentials']['user_id'] = user_id
            else:
                body['auth']['passwordCredentials']['username'] = user_name

            if password is not None:
                body['auth']['passwordCredentials']['password'] = password
        else:
            raise Exception('Insufficient credentials provided, missing '
                'user_id, username or token_id.')

        if tenant_id is not None:
            body['auth']['tenant_id'] = tenant_id
        elif tenant_name is not None:
            body['auth']['tenant_name'] = tenant_name

        return self._create(self.build_url(), body, 'access')

    def validate(self, token):
        return self._get(self.build_url(token_id=base.getid(token)), 'access')

    def revoke(self, token):
        return super(TokenManager, self).delete(
            token_id=base.getid(token))
