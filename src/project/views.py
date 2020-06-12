from django.shortcuts import render
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project, Team


class ProjectListView(LoginRequiredMixin,  UserPassesTestMixin, ListView):
    """
        Lists of Projects in a single view of a Specific Logged IN USER
    """
    model = Project
    template_name = 'project/project_list.html'
    context_object_name = 'projects'
    ordering = ['-title']
    paginate_by = 5


class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    template_name = 'project/project_create.html'


class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
        Details of the Project would have links to Detail Data
    """
    model = Project
    context_object_name = 'project'
    template_name = 'project/project_detail.html'


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    template_name = 'project/project_update.html'


class TeamListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Team
    template_name = 'proeject/team_list.html'


class TeamCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Team
    template_name = 'project/team_create.html'


class TeamDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
       Details of specific team in the website
    """
    model = Team
    template_name = 'project/team_detail.html'


class TeamUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
        Update The Team Details 
    """
    model = Team
    template_name = 'project/team_update.html'


class TeamListAllView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Lists all Teams in the whole website for Instructor's Mostly
    """
    model = Team
    template_name = 'project/team_listall.html'


class ProjectListAllView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    This view would list all teams in the whole website (mostly for )

    """
    model = Project
    template_name = 'project/project_listall.html'
