from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Logger, LogFile, LogURL
from django.contrib import messages
from project.models import Project
from django.db.models.query import QuerySet
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from uuid import UUID

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

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

    # Get a list of all teams that the user is a part of
    user_teams = request.user.team_set.all()
    project_list = []

    # Get a list of all projects that the user's teams have made
    for team in user_teams:
        [project_list.append(x) for x in team.project_set.all()]

    # pass in this list
    context = {
        "projects":project_list,
    }
    if request.method == "POST":
        log_title = request.POST.get('log-title', "")
        log_description = request.POST.get('log-description', "")
        log_content = request.POST.get('log-content', "")
        log_project = request.POST.get('selection', "")
        custom_password_true = request.POST.get('custom-password-check', "")
        
        if custom_password_true == "on":
            password = request.POST.get("custom-password", "")
        else:
            password = request.user.password.split('$')[-1]

        password=generatePassword(password)

        BLOCK_SIZE = 32
        encryption_suite = AES.new(generatePassword(password).encode(), AES.MODE_ECB)

        cipher_text = encryption_suite.encrypt(pad(log_content.encode(), BLOCK_SIZE)).hex()

        
        if log_project == "Personal Log":
            newlog = Logger.objects.create(
                title=log_title,
                short_description=log_description,
                note=cipher_text,
                user=request.user,
                password=password,
                
            )            
        else:
            project = Project.objects.get(title=log_project)
            newlog = Logger.objects.create(
                title=log_title,
                short_description=log_description,
                note=cipher_text,
                user=request.user,
                project=project,
                password=password,
                
            )

        messages.add_message(request, messages.SUCCESS, "Log Successfully created.")
        return redirect('log-list')
    return render(request, 'log/create_log.html', context=context)

def logDetailView(request, *args, **kwargs):

    logtoview = kwargs.get('pk')

    try:
        logtoview = UUID(str(logtoview))
    except ValueError:
        return HttpResponse("Error: Invalid log ID", status=400)
        

    try:
        thelog = Logger.objects.get(id=logtoview)
        password = thelog.password


        BLOCK_SIZE = 32
        encryption_suite = AES.new(password.encode(), AES.MODE_ECB)

        deciphered_text = encryption_suite.decrypt(bytes.fromhex(thelog.note)).decode()

        thelog.note = deciphered_text

        userlist = thelog.access.all()

        context = {
            "log":thelog,
            "userlist":userlist,
        }

        return render(request, 'log/view_log.html', context)

    except ObjectDoesNotExist:
        return HttpResponse("Error: Invalid log ID", status=400)
    except:
        messages.add_message(request, messages.ERROR, "Log data is corrupt. Decryption failed.")
        return redirect('log-list')



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


def logDeleteView(request):

    if request.method != "GET":
        return HttpResponse("Error: Invalid request", status=400)
    
    else:
        logtodelete = request.GET.get('id', "")

        try:
            logtodelete = UUID(logtodelete)
        except ValueError:
            return HttpResponse("Error: Invalid log ID", status=400)
            

        try:
            log = Logger.objects.get(id=logtodelete)
            log.published = False
            log.save()
            messages.add_message(request, messages.SUCCESS, "Log was successfully deleted.")
            return redirect("log-list")

            return HttpResponse(log)
        except ObjectDoesNotExist:
            return HttpResponse("Error: Invalid log ID", status=400)



def logListView(request):
    context = {
        "logs":Logger.objects.filter(user=request.user).filter(published=True).order_by('-date_created')
    }
    return render(request, 'log/list_view.html', context)
    


def logEditView(request, *args, **kwargs):

    logtoview = kwargs.get('pk')

    try:
        logtoview = UUID(str(logtoview))
    except ValueError:
        return HttpResponse("Error: Invalid log ID", status=400)
        

    try:
        thelog = Logger.objects.get(id=logtoview)
        password = thelog.password


        BLOCK_SIZE = 32
        encryption_suite = AES.new(password.encode(), AES.MODE_ECB)

        deciphered_text = encryption_suite.decrypt(bytes.fromhex(thelog.note)).decode()

        thelog.note = deciphered_text
    except ObjectDoesNotExist:
        return HttpResponse("Error: Invalid log ID", status=400)
    except:
        messages.add_message(request, messages.ERROR, "An Unknown error occurred.")
        return redirect('landing-page')

    if request.method == "POST":
        log_title = request.POST.get('log-title', "")
        log_description = request.POST.get('log-description', "")
        log_content = request.POST.get('log-content', "")

        # changelog = Logger.objects.
        BLOCK_SIZE = 32
        encryption_suite = AES.new(thelog.password.encode(), AES.MODE_ECB)

        cipher_text = encryption_suite.encrypt(pad(log_content.encode(), BLOCK_SIZE)).hex()

        thelog.title = log_title
        thelog.short_description=log_description
        thelog.note = cipher_text
        thelog.save()

        messages.add_message(request, messages.SUCCESS, "Log saved successfully.")
        return redirect('log-list')



    # Get a list of all teams that the user is a part of
    user_teams = request.user.team_set.all()
    project_list = []

    # Get a list of all projects that the user's teams have made
    for team in user_teams:
        [project_list.append(x) for x in team.project_set.all()]

    context = {
        "log":thelog,
        "projects":project_list,

    }



    return render(request, 'log/log_edit_view.html', context)


def recBinView(request):
    if request.method != "GET":
        return HttpResponse("Error: Invalid request", status=400)
    
    else:
        logtodelete = request.GET.get('id', "")

        if logtodelete == "":
            context = {
                "logs":Logger.objects.filter(user=request.user).filter(published=False).order_by('-date_created')
            }
            return render(request, 'log/bin_view.html', context)
        else:
            try:
                logtodelete = UUID(logtodelete)
            except ValueError:
                return HttpResponse("Error: Invalid log ID", status=400)
                

            try:
                log = Logger.objects.get(id=logtodelete)
                log.published = True
                log.save()
                messages.add_message(request, messages.SUCCESS, "Log was successfully recovered.")
                return redirect("log-list")

                return HttpResponse(log)
            except ObjectDoesNotExist:
                return HttpResponse("Error: Invalid log ID", status=400)


def generatePassword(unpaddedPassword):
    if len(unpaddedPassword) < 32:
        generated_padding = (32-len(unpaddedPassword))*"#"

        return unpaddedPassword + generated_padding
    
    elif len(unpaddedPassword) > 32:
        return unpaddedPassword[:32]
    
    else:
        return unpaddedPassword


@csrf_exempt
def shareController(request):
    if request.method == "POST":
        print(request.POST.dict())
    if request.method == "GET":
        pass
    
    return JsonResponse({"error":"not found"}, status=404)