import httplib2
import urlparse
import uuid

from keystoneclient.v3 import projects
from tests.v3 import utils


class ProjectTests(utils.TestCase, utils.CrudTests):
    def setUp(self):
        super(ProjectTests, self).setUp()
        self.additionalSetUp()
        self.key = 'project'
        self.collection_key = 'projects'
        self.model = projects.Project
        self.manager = self.client.projects

    def new_ref(self, **kwargs):
        kwargs = super(ProjectTests, self).new_ref(**kwargs)
        kwargs.setdefault('domain_id', uuid.uuid4().hex)
        kwargs.setdefault('enabled', True)
        kwargs.setdefault('name', uuid.uuid4().hex)
        return kwargs

    def test_list_projects_for_user(self):
        ref_list = [self.new_ref(), self.new_ref()]

        user_id = uuid.uuid4().hex
        resp = httplib2.Response({
            'status': 200,
            'body': self.serialize(ref_list),
        })

        method = 'GET'
        httplib2.Http.request(
            urlparse.urljoin(
                self.TEST_URL,
                'v3/users/%s/%s' % (user_id, self.collection_key)),
            method,
            headers=self.headers[method]) \
            .AndReturn((resp, resp['body']))
        self.mox.ReplayAll()

        returned_list = self.manager.list(user=user_id)
        self.assertTrue(len(returned_list))
        [self.assertTrue(isinstance(r, self.model)) for r in returned_list]
