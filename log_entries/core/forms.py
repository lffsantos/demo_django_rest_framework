import datetime
from django import forms
from log_entries.core.models import Category, Event


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(render_value=False))


class EventForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField(required=False)
    note = forms.CharField(max_length=255, required=False)
    category = forms.ModelChoiceField(Category.objects)

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

    def save(self, data, user):
        event = Event()
        start_date = datetime.datetime.strptime(data['start_date'], "%Y-%m-%d %H:%M")
        event.start_date = start_date
        if data['end_date']:
            event.end_date = datetime.datetime.strptime(data['end_date'], "%Y-%m-%d %H:%M")

        event.category_id = data['category']
        event.note = data['note']
        event.user = user
        event.save()