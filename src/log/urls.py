from django.urls import path
from . import views

urlpatterns = [
    path('log/create', views.LoggerCreateView.as_view(), name='log-create'),
    path('log/<uuid:pk>/detail',
         views.LoggerDetailView.as_view(), name='log-detail'),
    path('log/<uuid:pk>/update',
         views.LoggerUpdateView.as_view(), name='log-update'),
    path('log/', views.LoggerListView.as_view(), name='log-list'),
]
