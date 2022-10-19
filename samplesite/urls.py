from django.urls import path
from .views import index

ulrpatterns = [
    path('', index),
]

