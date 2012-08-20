import uuid

from keystoneclient.v3 import endpoints
from tests.v3 import utils


class EndpointTests(utils.TestCase, utils.CrudTests):
    def setUp(self):
        super(EndpointTests, self).setUp()
        self.additionalSetUp()
        self.key = 'endpoint'
        self.collection_key = 'endpoints'
        self.model = endpoints.Endpoint
        self.manager = self.client.endpoints

    def new_ref(self, **kwargs):
        kwargs = super(EndpointTests, self).new_ref(**kwargs)
        kwargs.setdefault('interface', uuid.uuid4().hex)
        kwargs.setdefault('service_id', uuid.uuid4().hex)
        kwargs.setdefault('url', uuid.uuid4().hex)
        return kwargs
