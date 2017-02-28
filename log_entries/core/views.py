from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r, get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from log_entries.core.auth import requires_auth
from log_entries.core.forms import LoginForm, EventForm
from log_entries.core.models import Category, Event
from log_entries.core.serializer import (
    CategorySerializer, UserSerializer, EventSerializer
)


@api_view(['GET'])
def categories(request):
    list_categories = Category.objects.all()
    serializer = CategorySerializer(list_categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@requires_auth
def me(request):
    user = User.objects.get(pk=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@requires_auth
def events(request):
    if request.method == 'GET':
        list_events = Event.objects.filter(user=request.user).order_by('start_date')
        serializer = EventSerializer(list_events, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        payload = request.data
        if not payload:
            return Response({'error': 'no send data'}, status=500)

        payload['user_id'] = request.user.id
        serializer = EventSerializer()
        event = serializer.create(serializer.to_internal_value(payload))
        return Response({'id': event.pk}, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
@requires_auth
def events_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.user != request.user:
        raise PermissionDenied()

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    if request.method == 'PUT':
        payload = request.data
        payload['user_id'] = request.user.id
        serializer = EventSerializer()
        serializer.update(event, serializer.to_internal_value(payload))
        return Response()

    if request.method == 'DELETE':
        event.delete()
        return Response()


def do_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def do_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(r('/'))

    log_form = LoginForm(request.POST)

    if request.method == 'GET'or not log_form.is_valid():
        return render(request, 'login.html', {'form': LoginForm()})


    username = log_form.cleaned_data['username']
    password = log_form.cleaned_data['password']

    try:
        u = User.objects.get(username=username)
    except ObjectDoesNotExist:
        messages.error(request,  'Invalid User or Password')
        return render(request, 'login.html', {'form': LoginForm()})

    usuario = authenticate(username=username, password=password)
    login(request, usuario)

    return HttpResponseRedirect(r('/'))


@login_required(login_url='/login/')
def home(request):
    events = Event.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'list_events.html', {'events': events})


@login_required(login_url='/login/')
def create_event(request):
    if request.method == 'GET':
        return render(
            request, 'event.html', {
                'categories': Category.objects.all()
            }
        )

    form_event = EventForm(request.POST or None)

    if form_event.is_valid():
        form_event.save(request.POST, request.user)

    return HttpResponseRedirect(r('/'))


@login_required(login_url='/login/')
def delete_event(request, pk):
    event = Event.objects.get(pk=pk)
    event.delete()
    return HttpResponseRedirect(r('/'))
