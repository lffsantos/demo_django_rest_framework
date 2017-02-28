from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from log_entries.core.models import Category, Event


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Category Name')

    def test_create(self):
        self.assertTrue(Category.objects.exists())


class EventModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='lffsantos', password='test',
                                        email='lffsantos@gmail.com')
        self.category = Category.objects.create(name='Category Name')
        self.event = Event.objects.create(
            start_date=datetime.now(), note='small note', category=self.category,
            user=self.user
        )

    def test_create(self):
        self.assertTrue(Category.objects.exists())