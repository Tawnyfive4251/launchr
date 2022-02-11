from django.urls import path

from .views import YoutubeTranscriber, TranscriptViewer
from . import views
urlpatterns = [
    path(
        route='youtube',
        view=YoutubeTranscriber.as_view(),
        name="youtube"
    ),
    path(
        route='upload',
        view=views.MediaTranscriber,
        name="media"
    ),
    path(
        route='viewer',
        view=TranscriptViewer.as_view(),
        name="viewer"
    ),
    ]