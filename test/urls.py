from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('check/',Check.as_view()),
    path('create/',CreateTip.as_view()),
    path('status/<str:task_id>/',TaskStatus.as_view()),
    path('delete/',DeleteTip.as_view()),
]