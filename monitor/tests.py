import unittest

from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home__index(self):
        from .views import home__index
        request = testing.DummyRequest()
        info = home__index(request)
        #self.assertEqual(info['project'], 'monitor')


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from monitor import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'Monitor' in res.body)
