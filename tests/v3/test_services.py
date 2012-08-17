import urlparse
import json

import httplib2

from keystoneclient.v3 import services
from tests.v3 import utils


class ServiceTests(utils.TestCase):
    def setUp(self):
        super(ServiceTests, self).setUp()
        self.TEST_REQUEST_HEADERS = {
            'X-Auth-Token': 'aToken',
            'User-Agent': 'python-keystoneclient',
        }
        self.TEST_POST_HEADERS = {
            'Content-Type': 'application/json',
            'X-Auth-Token': 'aToken',
            'User-Agent': 'python-keystoneclient',
        }
        self.TEST_services = {
            'services': [
                {
                    'id': '1',
                    'type': 'compute',
                },
                {
                    'id': '3',
                    'type': 'identity',
                }
            ],
        }

    def test_create(self):
        req = self.TEST_services['services'][0].copy()
        del req['id']
        resp = httplib2.Response({
            'status': 201,
            'body': json.dumps({'service': self.TEST_services['services'][0]}),
        })

        httplib2.Http.request(urlparse.urljoin(self.TEST_URL,
                              'v3/services'),
                              'POST',
                              body=json.dumps({'service': req}),
                              headers=self.TEST_POST_HEADERS) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        service = self.client.services.create(
            type=req['type'])
        self.assertTrue(isinstance(service, services.Service))
        self.assertEqual(service.id, self.TEST_services['services'][0]['id'])
        self.assertEqual(service.type, req['type'])

    def test_get(self):
        ref = self.TEST_services['services'][0]
        resp = httplib2.Response({
            'status': 200,
            'body': json.dumps({
                'service': ref,
            }),
        })
        httplib2.Http.request(urlparse.urljoin(self.TEST_URL,
                              'v3/services/%s' % ref['id']),
                              'GET',
                              headers=self.TEST_REQUEST_HEADERS) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        service = self.client.services.get(ref['id'])
        self.assertTrue(isinstance(service, services.Service))
        self.assertEqual(service.id, ref['id'])
        self.assertEqual(service.type, ref['type'])

    def test_list(self):
        resp = httplib2.Response({
            'status': 200,
            'body': json.dumps(self.TEST_services),
        })

        httplib2.Http.request(urlparse.urljoin(self.TEST_URL,
                              'v3/services'),
                              'GET',
                              headers=self.TEST_REQUEST_HEADERS) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        service_list = self.client.services.list()
        [self.assertTrue(isinstance(r, services.Service)) for r in service_list]

    def test_update(self):
        req = self.TEST_services['services'][0].copy()
        del req['id']
        resp = httplib2.Response({
            'status': 200,
            'body': json.dumps({'service': self.TEST_services['services'][0]}),
        })

        httplib2.Http.request(urlparse.urljoin(self.TEST_URL,
                              'v3/services/1'),
                              'PATCH',
                              body=json.dumps({'service': req}),
                              headers=self.TEST_POST_HEADERS) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        service = self.client.services.update('1', type=req['type'])
        self.assertTrue(isinstance(service, services.Service))
        self.assertEqual(service.id, self.TEST_services['services'][0]['id'])
        self.assertEqual(service.type, req['type'])

    def test_delete(self):
        resp = httplib2.Response({
            'status': 200,
            'body': '',
        })
        httplib2.Http.request(urlparse.urljoin(self.TEST_URL,
                              'v3/services/1'),
                              'DELETE',
                              headers=self.TEST_REQUEST_HEADERS) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        self.client.services.delete('1')
