from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Logger, LogFile, LogURL
from django.contrib import messages

from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


@login_required
def CreateNote(request):
    if request.method == "POST":
        logtext = request.POST.get('logdata', False)
        newlog = Logger.objects.create(
            title="Test log",
            note=logtext,
            user=request.user,
            isNote=True
        )
        newlog.save()

        messages.success(request, 'Your log has been created')
        # return redirect('home')
    return render(request, 'user/createlog.html')


class LoggerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Create Logger  Object in backend
    """
    model = Logger
    template_name_name = 'log/logger_create.html'


class LoggerDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Logger


class LoggerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update Log
    """
    model = Logger
    template_name = 'log/logger_update.html'


class LoggerListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Display All Logs from User 
    """
    model = Logger
    template_name = 'log/logger_list.html'


class LoggerUnPublish(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Confirms From User if Truly They want to unpublish said log
    """
    model = Logger
    template_name = 'log/logger_unpublish.html'
