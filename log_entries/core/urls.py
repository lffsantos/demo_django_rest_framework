from django.conf.urls import url
from log_entries.core.views import categories, me, events, events_detail

urlpatterns = [
    url(r'categories/$', categories, name='categories'),
    url(r'me/$', me, name='me'),
    url(r'events/$', events),
    url(r'events/(?P<event_id>\d+)/$', events_detail),
]
