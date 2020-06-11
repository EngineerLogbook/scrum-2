from django.shortcuts import render
from django.http import JsonResponse
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


# @login_required
# def CreateNote(request):
#     if request.method == "POST":
#         logtext = request.POST.get('logdata', False)
#         newlog = Logger.objects.create(
#             title="Test log",
#             note=logtext,
#             user=request.user,
#             isNote=True
#         )
#         newlog.save()

#         messages.success(request, 'Your log has been created')
#         # return redirect('home')
#     return render(request, 'user/createlog.html')


class LoggerCreateView(LoginRequiredMixin, CreateView):
    """
    Create Logger  Object in backend
    """
    model = Logger
    template_name = 'log/logger_create.html'
    fields = ['title', 'note', 'project', 'short_description', 'password']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class LoggerDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Logger
    template_name = 'log/logger_detail.html'


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


def logCreateView(request):
    if request.method == "POST":
        print(request.POST.dict())
    return render(request, 'log/create_log.html', context={})


def fileUploadHandler(request):
    if request.method == "POST":
        print(request.POST.dict())
        filetoupload = request.FILES['file']

        savedfile = LogFile.objects.create(file=filetoupload, title=filetoupload.name)
        SITE_PROTOCOL = 'http://'
        if request.is_secure():
            SITE_PROTOCOL = 'https://'
        
        return JsonResponse({"message": "File uploaded.", "link":SITE_PROTOCOL + request.META['HTTP_HOST'] + savedfile.file.url})
    if request.method == "GET":
        return JsonResponse({"message":"Get method not allowed"})        