from django.contrib.auth.models import User
from django.test import TestCase
from log_entries.core.models import Category, Event
from log_entries.core.serializer import CategorySerializer, UserSerializer, \
    EventSerializer
from model_mommy import mommy
from rest_framework.exceptions import ValidationError


class TestCategorySerializer(TestCase):

    def setUp(self):
        self.category = mommy.make(Category, name='category')

    def test_to_representation(self):
        serializer = CategorySerializer()
        assert {'name': 'category'} == serializer.to_representation(self.category)


class TestUserSerializer(TestCase):

    def setUp(self):
        self.user = mommy.make(User, first_name='new', last_name='user')

    def test_to_representation(self):
        serializer = UserSerializer()
        assert {'full_name': 'new user'} == serializer.to_representation(self.user)


class TestEventSerializer(TestCase):

    def setUp(self):
        self.category = mommy.make(Category, name='category')
        self.user = mommy.make(User, first_name='new', last_name='user')
        self.event = mommy.make(
            Event, start_date='2010-01-01 08:00', note='test', category=self.category,
            end_date=None, user=self.user
        )
        self.serializer = EventSerializer()

    def test_to_representation(self):
        expected = {
            'start_date': '2010-01-01 08:00', 'end_date': None,
            'note': 'test',
            'category': {
                'name': 'category'
            },
        }
        assert expected == self.serializer.to_representation(self.event)

    def test_to_internal_value_all_valid(self):
        payload = {
            'start_date': '2010-01-01 08:00',
            'end_date': None,
            'note': 'test',
            'category_id': self.category.id,
            'user_id': self.user.id
        }

        expected = self.serializer.to_internal_value(payload)
        expected_count = 0
        for key, value in payload.items():
            if expected.get(key) == value:
                expected_count += 1

        assert expected_count == 5

    def test_to_internal_invalid_category(self):
        payload = {
            'start_date': '2010-01-01 08:00',
            'end_date': None,
            'note': 'test',
            'category_id': 6,
            'user_id': self.user.id
        }
        with self.assertRaises(ValidationError) as error:
            self.serializer.to_internal_value(payload)

        assert error.exception.detail == {'category': 'Invalid Category'}

    def test_to_internal_invalid_note(self):
        payload = {
            'start_date': '2010-01-01 08:00',
            'end_date': None,
            'note': '0'*256,
            'category_id': self.category.id,
            'user_id': self.user.id
        }
        with self.assertRaises(ValidationError) as error:
            self.serializer.to_internal_value(payload)

        assert error.exception.detail == {'note': 'May not be more than 255 characters.'}

    def test_to_internal_not_start_date(self):
        payload = {
            'start_date': '',
            'end_date': None,
            'note': '0'*256,
            'category_id': self.category.id,
            'user_id': self.user.id
        }
        with self.assertRaises(ValidationError) as error:
            self.serializer.to_internal_value(payload)

        assert error.exception.detail == {'start_date': 'This field is required.'}

    def test_create(self):
        payload = {
            'start_date': '2010-01-01 08:00', 'end_date': None,
            'note': 'test',
            'category_id': self.category.id,
            'user_id': self.user.id
        }
        event = self.serializer.create(payload)
        assert len(Event.objects.filter(id=event.pk)) == 1

    def test_update(self):
        payload = {
            'start_date': '2010-01-01 08:00',
            'end_date': '2010-01-01 12:00',
            'note': 'update_note add end_date',
            'category_id': self.category.id,
            'user_id': self.user.id
        }
        _event = self.serializer.update(self.event, payload)
        for key, value in payload.items():
            assert _event.__dict__[key] == value