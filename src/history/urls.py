from django.urls import path
from .views import *
urlpatterns = [
    
    path('history', userHistoryView, name='user-history'),
    path('history_all', completeHistoryView, name='complete-history'),
]
