from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.urls import resolve
from django.contrib import messages
from django.utils.translation import ugettext as _
from .forms import ReportSuggestionForm
from .models import UserMessage
# Create your views here.
from datetime import datetime, timedelta
import json


def user_messages(request):
    time = datetime.now() - timedelta(hours=5)
    message_exists = UserMessage.objects.filter(
        user=request.user,
        created_at__gt=time
    )

    if request.method == 'POST':
        form = ReportSuggestionForm(request.POST)

        if message_exists:
            messages.error(request, _('1 msg in 5h'))
            django_messages = [
                {'level': x.level,
                 'message': x.message,
                 'tags': x.tags} for x in messages.get_messages(request)]

            data = {'messages': django_messages}
            return JsonResponse(data)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, _('srabotalo'))

            django_messages = [
                {'level': x.level,
                 'message': x.message,
                 'tags': x.tags} for x in messages.get_messages(request)]

            data = {'messages': django_messages}
            return JsonResponse(data)

    if request.method == 'GET':
        form = ReportSuggestionForm()
        return render(request, 'home/suggestions.html', {'form': form})