import json
import urlparse
import uuid

import httplib2

from keystoneclient.v3 import users
from tests.v3 import utils


class CrudTests(object):
    key = None
    collection_key = None
    model = None
    manager = None

    def get_ref(self, **kwargs):
        kwargs.setdefault('id', uuid.uuid4().hex)
        kwargs.setdefault('name', uuid.uuid4().hex)
        kwargs.setdefault('description', uuid.uuid4().hex)
        kwargs.setdefault('enabled', True)
        return kwargs

    def additionalSetUp(self):
        self.headers = {
            'GET': {
                'X-Auth-Token': 'aToken',
                'User-Agent': 'python-keystoneclient',
            }
        }

        self.headers['DELETE'] = self.headers['GET'].copy()
        self.headers['POST'] = self.headers['GET'].copy()
        self.headers['POST']['Content-Type'] = 'application/json'
        self.headers['PATCH'] = self.headers['POST'].copy()

    def serialize(self, entity):
        if isinstance(entity, dict):
            return json.dumps({self.key: entity}, sort_keys=True)
        if isinstance(entity, list):
            return json.dumps({self.collection_key: entity}, sort_keys=True)
        raise NotImplementedError('Are you sure you want to serialize that?')

    def test_create(self):
        ref = self.get_ref()
        resp = httplib2.Response({
            'status': 201,
            'body': self.serialize(ref),
        })

        method = 'POST'
        req_ref = ref.copy()
        req_ref.pop('id')
        httplib2.Http.request(
            urlparse.urljoin(
                self.TEST_URL,
                'v3/%s' % self.collection_key),
            method,
            body=self.serialize(req_ref),
            headers=self.headers[method]) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        returned = self.manager.create(**req_ref)
        self.assertTrue(isinstance(returned, self.model))
        for attr in ref:
            self.assertEqual(getattr(returned, attr), ref[attr],
                'Expected different %s' % attr)

    def test_get(self):
        ref = self.get_ref()
        resp = httplib2.Response({
            'status': 200,
            'body': self.serialize(ref),
        })
        method = 'GET'
        httplib2.Http.request(
            urlparse.urljoin(
                self.TEST_URL,
                'v3/%s/%s' % (self.collection_key, ref['id'])),
            method,
            headers=self.headers[method]) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        returned = self.manager.get(ref['id'])
        self.assertTrue(isinstance(returned, self.model))
        for attr in ref:
            self.assertEqual(getattr(returned, attr), ref[attr],
                'Expected different %s' % attr)

    def test_list(self):
        ref_list = [self.get_ref(), self.get_ref()]

        resp = httplib2.Response({
            'status': 200,
            'body': self.serialize(ref_list),
        })

        method = 'GET'
        httplib2.Http.request(
            urlparse.urljoin(
                self.TEST_URL,
                'v3/%s' % self.collection_key),
            method,
            headers=self.headers[method]) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        returned_list = self.manager.list()
        self.assertTrue(len(returned_list))
        [self.assertTrue(isinstance(r, self.model)) for r in returned_list]

    def test_update(self):
        ref = self.get_ref()
        req_ref = ref.copy()
        del req_ref['id']

        resp = httplib2.Response({
            'status': 200,
            'body': self.serialize(ref),
        })

        method = 'PATCH'
        httplib2.Http.request(
            urlparse.urljoin(
                self.TEST_URL,
                'v3/%s/%s' % (self.collection_key, ref['id'])),
            method,
            body=self.serialize(req_ref),
            headers=self.headers[method]) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        returned = self.manager.update(
            ref['id'],
            **req_ref)
        self.assertTrue(isinstance(returned, self.model))
        for attr in ref:
            self.assertEqual(getattr(returned, attr), ref[attr],
                'Expected different %s' % attr)

    def test_delete(self):
        ref = self.get_ref()
        method = 'DELETE'
        resp = httplib2.Response({
            'status': 204,
            'body': '',
        })
        httplib2.Http.request(
            urlparse.urljoin(
                self.TEST_URL,
                'v3/%s/%s' % (self.collection_key, ref['id'])),
            method,
            headers=self.headers[method]) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        self.manager.delete(ref['id'])


class UserTests(utils.TestCase, CrudTests):
    def setUp(self):
        super(UserTests, self).setUp()
        self.additionalSetUp()
        self.key = 'user'
        self.collection_key = 'users'
        self.model = users.User
        self.manager = self.client.users
