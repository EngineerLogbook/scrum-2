from django.urls import path
from . import views

urlpatterns = [
    path('log/create', views.logCreateView, name='log-create'),
    path('log/<uuid:pk>/detail',
         views.logDetailView, name='log-detail'),
    path('log/<uuid:pk>/edit',
         views.logEditView, name='log-edit'),
    path('log/', views.logListView, name='log-list'),
    path('log/uploadfile', views.fileUploadHandler, name='file-upload'),
    path('log/delete', views.logDeleteView, name='log-delete')
]
