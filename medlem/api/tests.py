import json

import mock

from django.test import TestCase
from django.core.urlresolvers import reverse


class TestAPI(TestCase):

    @mock.patch('ldap.initialize')
    def test_exists(self, mocked_initialize):
        connection = mock.MagicMock()
        mocked_initialize.return_value = connection

        url = reverse('api:exists')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

        # check that 400 Bad Request errors are proper JSON
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(
            json.loads(response.content),
            {'error': "missing key 'mail'"}
        )

        response = self.client.get(url, {'mail': ''})
        self.assertEqual(response.status_code, 400)

        result = {
            'abc123': {'uid': 'abc123', 'mail': 'peter@example.com'},
        }

        def search_s(base, scope, filterstr, *args, **kwargs):
            if 'peter@example.com' in filterstr:
                # if 'hgaccountenabled=TRUE' in filterstr:
                #     return []
                return result.items()
            return []

        connection.search_s.side_effect = search_s

        response = self.client.get(url, {'mail': 'peter@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), True)

        response = self.client.get(url, {'mail': 'never@heard.of.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), False)

        # response = self.client.get(url, {'mail': 'peter@example.com',
        #                                  'hgaccountenabled': ''})
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(json.loads(response.content), False)

        response = self.client.get(url, {'mail': 'peter@example.com',
                                         'gender': 'male'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), True)

    @mock.patch('ldap.initialize')
    def test_employee(self, mocked_initialize):
        connection = mock.MagicMock()
        mocked_initialize.return_value = connection

        url = reverse('api:employee')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

        response = self.client.get(url, {'mail': ''})
        self.assertEqual(response.status_code, 400)

        result = {
            'abc123': {'uid': 'abc123',
                       'mail': 'peter@mozilla.com',
                       'sn': u'B\xe3ngtsson'},
        }

        def search_s(base, scope, filterstr, *args, **kwargs):
            if 'peter@example.com' in filterstr:
                return result.items()
            return []

        connection.search_s.side_effect = search_s

        response = self.client.get(url, {'mail': 'peter@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), True)

        response = self.client.get(url, {'mail': 'never@heard.of.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), False)

    @mock.patch('ldap.initialize')
    def test_ingroup(self, mocked_initialize):
        connection = mock.MagicMock()
        mocked_initialize.return_value = connection

        url = reverse('api:in-group')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

        response = self.client.get(url, {'mail': ''})
        self.assertEqual(response.status_code, 400)

        response = self.client.get(url, {'mail': 'peter@example.com'})
        self.assertEqual(response.status_code, 400)

        response = self.client.get(url, {'mail': 'peter@example.com',
                                         'cn': ''})
        self.assertEqual(response.status_code, 400)

        result = {
            'abc123': {'uid': 'abc123', 'mail': 'peter@example.com'},
        }

        def search_s(base, scope, filterstr, *args, **kwargs):
            if 'ou=groups' in base:
                if (
                    'peter@example.com' in filterstr and
                    'cn=CrashStats' in filterstr
                ):
                    return result.items()
            else:
                # basic lookup
                if 'peter@example.com' in filterstr:
                    return result.items()
            return []

        connection.search_s.side_effect = search_s

        response = self.client.get(url, {'mail': 'not@head.of.com',
                                         'cn': 'CrashStats'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), False)

        response = self.client.get(url, {'mail': 'peter@example.com',
                                         'cn': 'CrashStats'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), True)

        response = self.client.get(url, {'mail': 'peter@example.com',
                                         'cn': 'NotInGroup'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), False)
