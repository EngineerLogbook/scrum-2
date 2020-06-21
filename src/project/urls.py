from django.urls import path
from . import views

urlpatterns = [
    path('project/create', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<uuid:pk>/detail',
         views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<uuid:pk>/update',
         views.ProjectUpdateView.as_view(), name='project-update'),
    path('project/', views.projectListView, name='project-list'),
    path('project/all', views.ProjectListAllView.as_view(), name='project-listall'),

    path('team/create', views.TeamCreateView.as_view(), name='team-create'),
    path('team/<uuid:pk>/detail',
         views.TeamDetailView.as_view(), name='team-detail'),
    path('team/<uuid:pk>/update',
         views.TeamUpdateView.as_view(), name='team-update'),
    path('team/', views.TeamListView.as_view(), name='team-list'),
    path('team/all', views.TeamListAllView.as_view(), name='team-listall')
]
