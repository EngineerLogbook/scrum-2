from django.urls import path
from .views import landingView


urlpatterns = [
    path('', landingView, name='home')
]
