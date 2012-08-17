import urlparse
import json

import httplib2

from keystoneclient.v3 import domains
from tests.v3 import utils


class DomainTests(utils.TestCase):
    def setUp(self):
        super(DomainTests, self).setUp()
        self.TEST_REQUEST_HEADERS = {
            'X-Auth-Token': 'aToken',
            'User-Agent': 'python-keystoneclient',
        }
        self.TEST_POST_HEADERS = {
            'Content-Type': 'application/json',
            'X-Auth-Token': 'aToken',
            'User-Agent': 'python-keystoneclient',
        }
        self.TEST_DOMAINS = {
            'domains': [
                {
                    'id': '1',
                    'name': 'default',
                    'description': 'Foo',
                    'enabled': True,
                },
                {
                    'id': '3',
                    'name': 'custom',
                    'description': 'Bar',
                    'enabled': False,
                }
            ],
        }

    def test_create(self):
        req = self.TEST_DOMAINS['domains'][0].copy()
        del req['id']
        resp = httplib2.Response({
            'status': 201,
            'body': json.dumps({'domain': self.TEST_DOMAINS['domains'][0]}),
        })

        httplib2.Http.request(urlparse.urljoin(self.TEST_URL,
                              'v3/domains'),
                              'POST',
                              body=json.dumps({'domain': req}),
                              headers=self.TEST_POST_HEADERS) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        domain = self.client.domains.create(
            name=req['name'],
            description=req['description'],
            enabled=req['enabled'])
        self.assertTrue(isinstance(domain, domains.Domain))
        self.assertEqual(domain.id, self.TEST_DOMAINS['domains'][0]['id'])
        self.assertEqual(domain.name, req['name'])
        self.assertEqual(domain.description, req['description'])
        self.assertEqual(domain.enabled, req['enabled'])

    def test_get(self):
        ref = self.TEST_DOMAINS['domains'][0]
        resp = httplib2.Response({
            'status': 200,
            'body': json.dumps({
                'domain': ref,
            }),
        })
        httplib2.Http.request(urlparse.urljoin(self.TEST_URL,
                              'v3/domains/%s' % ref['id']),
                              'GET',
                              headers=self.TEST_REQUEST_HEADERS) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        domain = self.client.domains.get(ref['id'])
        self.assertTrue(isinstance(domain, domains.Domain))
        self.assertEqual(domain.id, ref['id'])
        self.assertEqual(domain.name, ref['name'])
        self.assertEqual(domain.description, ref['description'])
        self.assertEqual(domain.enabled, ref['enabled'])

    def test_list(self):
        resp = httplib2.Response({
            'status': 200,
            'body': json.dumps(self.TEST_DOMAINS),
        })

        httplib2.Http.request(urlparse.urljoin(self.TEST_URL,
                              'v3/domains'),
                              'GET',
                              headers=self.TEST_REQUEST_HEADERS) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        domain_list = self.client.domains.list()
        [self.assertTrue(isinstance(r, domains.Domain)) for r in domain_list]

    def test_update(self):
        req = self.TEST_DOMAINS['domains'][0].copy()
        del req['id']
        del req['name']
        del req['enabled']
        resp = httplib2.Response({
            'status': 200,
            'body': json.dumps({'domain': self.TEST_DOMAINS['domains'][0]}),
        })

        httplib2.Http.request(urlparse.urljoin(self.TEST_URL,
                              'v3/domains/1'),
                              'PATCH',
                              body=json.dumps({'domain': req}),
                              headers=self.TEST_POST_HEADERS) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        domain = self.client.domains.update('1', description=req['description'])
        self.assertTrue(isinstance(domain, domains.Domain))
        self.assertEqual(domain.id, self.TEST_DOMAINS['domains'][0]['id'])
        self.assertEqual(domain.name, self.TEST_DOMAINS['domains'][0]['name'])
        self.assertEqual(domain.description, self.TEST_DOMAINS['domains'][0]['description'])
        self.assertEqual(domain.enabled, self.TEST_DOMAINS['domains'][0]['enabled'])

    def test_delete(self):
        resp = httplib2.Response({
            'status': 200,
            'body': '',
        })
        httplib2.Http.request(urlparse.urljoin(self.TEST_URL,
                              'v3/domains/1'),
                              'DELETE',
                              headers=self.TEST_REQUEST_HEADERS) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        self.client.domains.delete('1')
