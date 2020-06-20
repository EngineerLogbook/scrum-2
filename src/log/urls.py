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
    path('log/delete', views.logDeleteView, name='log-delete'),
    path('log/bin', views.recBinView, name='log-bin'),
    path('log/share', views.shareController, name='log-share'),
    path('log/shared', views.mySharesView, name='shared-with-me'),
    path('log/search', views.searchResults, name='search-results'),
]
