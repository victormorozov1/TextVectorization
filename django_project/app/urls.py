from django.urls import path

from .views import ask_question

urlpatterns = [
    path('ask_question', ask_question)
]
