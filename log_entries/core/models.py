from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    name = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.name

    @property
    def serialize(self):
        return {
            'name': self.name,
        }


class Event(models.Model):

    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=255)
    category = models.ForeignKey('Category')
    user = models.ForeignKey(User)

    def __str__(self):
        return "{} - {} - {}".format(self.start_date, self.end_date, self.note)


