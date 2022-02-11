from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from flask import request

import stripe
from allauth.account.views import (
    PasswordChangeView as AllauthPasswordChangeView,
    EmailView as AllauthEmailView,
)
from allauth.account.adapter import get_adapter
from allauth.account import signals
from allauth.account.models import EmailAddress
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView
from djstripe.models import Customer
from users.forms import AccountForm
from users.email import subscribe_to_mailing_list, unsubscribe_from_mailing_list
from django.views.decorators.http import require_http_methods
from . import models
from . import tasks


# Create your views here.
class YoutubeTranscriber(LoginRequiredMixin, TemplateView):
    template_name = "users/youtubeupload.html"

@require_http_methods(['GET', 'POST'])
def MediaTranscriber(request):
    """
    Main Home page
    """
    try:

        # GET method, return HTML page
        if request.method == 'GET':
            samples = models.AudioDataModel.objects.all()

            pending_jobs = samples.filter(status='PEN').count()
            show_timer = False
            if pending_jobs > 0:
                show_timer = True
            return render(request, 'transcriber/testing.html', {'samples': samples, 'show_timer': show_timer})

        # POST request, process the uploaded Audio file
        else:
            uploaded_file = request.FILES['uploaded_file']
            audio_data = models.AudioDataModel.objects.create(uploaded_file=uploaded_file)

        # Begin processing
        x = tasks.process_uploaded_file.delay(audio_data.id)

        return HttpResponse(json.dumps({'status': 'OK', 'passed':"async testing now"}), content_type="application/json")

    except Exception as e:
        if type(audio_data) is not None:
            audio_data.status = 'ERR'
            audio_data.error_occurred = True
            audio_data.error_message = str(e)
            audio_data.save()

        return HttpResponse(f'Error: {str(e)}')


class TranscriptViewer(LoginRequiredMixin, TemplateView):
    template_name = "users/youtubeupload.html"


