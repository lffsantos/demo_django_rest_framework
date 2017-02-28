from django.contrib.auth.models import User
from django.test import TestCase
from log_entries.core.models import Category, Event
from model_mommy import mommy
from rest_framework.test import RequestsClient, APIClient, APIRequestFactory


class TestCategories(TestCase):

    def setUp(self):
        self.category1 = mommy.make(Category)
        self.category2 = mommy.make(Category)
        self.response = self.client.get('http://testserver/api/v1/categories/')

    def test_list_categories(self):
        assert self.response.status_code == 200
        assert len(self.response.json()) == 2


class TestEvents(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = mommy.make(Category, _quantity=3)
        self.user = mommy.make(User, _quantity=2)
        self.event1 = mommy.make(Event, category=self.category[0], user=self.user[0])
        self.event2 = mommy.make(Event, category=self.category[0], user=self.user[1])
        self.event3 = mommy.make(Event, category=self.category[1], user=self.user[0])

    def _require_login(self):
        self.user[0].set_password('12345')
        self.user[0].save()
        self.client.login(username=self.user[0].username, password='12345')

    def test_events_unauthorized_access(self):
        response = self.client.get('/api/v1/events/')
        assert response.status_code == 401

    def test_events_get(self):
        self._require_login()
        self.response = self.client.get('/api/v1/events/')
        assert self.response.status_code == 200
        assert len(self.response.json()) == 2

    def test_events_post_error_no_payload(self):
        self._require_login()
        self.response = self.client.post('/api/v1/events/', {}, format='json')
        assert self.response.status_code == 500

    def test_events_post_valid(self):
        self._require_login()
        self.response = self.client.post('/api/v1/events/', {
            "start_date": "2014-01-01 08:00",
            "category_id": self.category[0].id,
            "note": "note test",
            "end_date": "2014-01-02 10:00",
        }, format='json')
        assert self.response.status_code == 201
        assert Event.objects.count() == 4


class TestMe(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = mommy.make(User, first_name='lucas', last_name='farias')

    def _require_login(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(username=self.user.username, password='12345')

    def test_me(self):
        self._require_login()
        self.response = self.client.get('/api/v1/me/')
        assert self.response.status_code == 200
        assert self.response.json()['full_name'] == "{} {}".format(
            self.user.first_name, self.user.last_name
        )
