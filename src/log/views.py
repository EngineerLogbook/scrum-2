from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Logger, LogFile, LogURL
from django.contrib import messages
from project.models import Project
from django.db.models.query import QuerySet
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from uuid import UUID
from django.urls import reverse
from django.db.models import Q
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
import re
import os
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import pathlib
import secrets
from engbook.settings.base_settings import BASE_DIR
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


@login_required
def logCreateView(request):

    user_teams = request.user.team_set.all()
    project_list = []

    for team in user_teams:
        project_list.append(team)


    # pass in this list
    context = {
<<<<<<< HEAD
        "teams": project_list,
        "files":LogFile.objects.filter(user=request.user),
=======
        "projects": project_list,
        "files": LogFile.objects.filter(user=request.user),
>>>>>>> upstream/master

    }
    if request.method == "POST":
        log_title = request.POST.get('log-title', "")
        log_description = request.POST.get('log-description', "")
        log_content = request.POST.get('log-content', "")
        log_project = request.POST.get('selection',"")
        custom_password_true = request.POST.get('custom-password-check', "")

        if custom_password_true == "on":
            password = request.POST.get("custom-password", "")
        else:
            password = request.user.password.split('$')[-1]

        password = generatePassword(password)

        BLOCK_SIZE = 32
        encryption_suite = AES.new(
            generatePassword(password).encode(), AES.MODE_ECB)
<<<<<<< HEAD

        cipher_text = encryption_suite.encrypt(
            pad(log_content.encode(), BLOCK_SIZE)).hex()

=======

        cipher_text = encryption_suite.encrypt(
            pad(log_content.encode(), BLOCK_SIZE)).hex()
>>>>>>> upstream/master

        if log_project == "Personal Log":
            newlog = Logger.objects.create(
                title=log_title,
                short_description=log_description,
                note=cipher_text,
                user=request.user,
                password=password,

            )
        else:
            project = Project.objects.get(id=log_project)
            newlog = Logger.objects.create(
                title=log_title,
                short_description=log_description,
                note=cipher_text,
                user=request.user,
                project=project,
                password=password,

            )

<<<<<<< HEAD
        messages.add_message(request, messages.SUCCESS, "Log Successfully created.")
        return redirect('logs-all')

    return render(request, 'log/create_log.html', context=context)

=======
        messages.add_message(request, messages.SUCCESS,
                             "Log Successfully created.")
        return redirect('log-list')

    return render(request, 'log/create_log.html', context=context)


>>>>>>> upstream/master
@login_required
def logDetailView(request, *args, **kwargs):

    logtoview = kwargs.get('pk')

    try:
        logtoview = UUID(str(logtoview))
    except ValueError:
        return HttpResponse("Error: Invalid log ID", status=400)
<<<<<<< HEAD

=======
>>>>>>> upstream/master

    try:
        thelog = Logger.objects.get(id=logtoview)

        allowedusers = []

        allowedusers.append(thelog.user)

        for users in thelog.access.all():
            allowedusers.append(users)

        if thelog.project:
            if (request.user.team_set.all() & thelog.project.team_set.all()).exists():
                allowedusers.append(request.user)
            pass

        if request.user not in allowedusers:
            return render(request, 'common/404.html', {})

        password = thelog.password

        BLOCK_SIZE = 32
        encryption_suite = AES.new(password.encode(), AES.MODE_ECB)

        deciphered_text = encryption_suite.decrypt(bytes.fromhex(thelog.note))
        padding = deciphered_text[-1]
        deciphered_text = deciphered_text[:-padding].decode()

        thelog.note = deciphered_text
<<<<<<< HEAD


=======
>>>>>>> upstream/master

        userlist = thelog.access.all()

        context = {
            "log": thelog,
            "userlist": userlist,
            "files": LogFile.objects.filter(user=request.user),
        }

        return render(request, 'log/view_log.html', context)

    except ObjectDoesNotExist:
        return HttpResponse("Error: Invalid log ID", status=400)
    except Exception as ಠ_ಠ:
        print(ಠ_ಠ)
        messages.add_message(request, messages.ERROR,
                             "Log data is corrupt. Decryption failed.")
        return redirect('log-list')


@login_required
def fileUploadHandler(request):
    if request.method == "POST":
        filetoupload = request.FILES['file']

#         try:
#             filesize = int(request.COOKIES['filesize'])
#             if filesize > 25000000:
#                 return JsonResponse({"message":"File exceeds 25 MB Limit."},status=413)

#         except Exception as e:
#             print(e)
#             return JsonResponse({"message":"Bad Request"}, status=400)

        file_extension = pathlib.Path(filetoupload.name).suffix
        file_name = filetoupload.name
        filetoupload.name = secrets.token_hex(10) + file_extension
        savedfile = LogFile.objects.create(
            file=filetoupload, title=file_name, user=request.user)
        SITE_PROTOCOL = 'http://'
        if request.is_secure():
            SITE_PROTOCOL = 'https://'

<<<<<<< HEAD
        return JsonResponse({"message": "File uploaded.", "link":SITE_PROTOCOL + request.META['HTTP_HOST'] + savedfile.file.url})
    if request.method == "GET":
        return JsonResponse({"message":"Get method not allowed"})
=======
        return JsonResponse({"message": "File uploaded.", "link": SITE_PROTOCOL + request.META['HTTP_HOST'] + savedfile.file.url})
    if request.method == "GET":
        return JsonResponse({"message": "Get method not allowed"})

>>>>>>> upstream/master

@login_required
def logDeleteView(request):

    if request.method != "GET":
        return HttpResponse("Error: Invalid request", status=400)

    else:
        logtodelete = request.GET.get('id', "")

        try:
            logtodelete = UUID(logtodelete)
        except ValueError:
            return HttpResponse("Error: Invalid log ID", status=400)
<<<<<<< HEAD

=======
>>>>>>> upstream/master

        try:
            log = Logger.objects.get(id=logtodelete)
            log.published = False
            log.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Log was successfully deleted.")
            return redirect("log-list")

            return HttpResponse(log)
        except ObjectDoesNotExist:
            return HttpResponse("Error: Invalid log ID", status=400)


@login_required
def logListView(request):
    context = {
        "logs": Logger.objects.filter(user=request.user, project=None).filter(published=True).order_by('-date_created'),
        "page_title": "Personal logs:",
        "userpage": True,
        "personal": True,
        "welcomemessage": 'Create your first log by clicking on the "New Log" Button !',
    }
    return render(request, 'log/list_view.html', context)

<<<<<<< HEAD
=======

>>>>>>> upstream/master
@login_required
def allLogsView(request, id):
    teams = request.user.team_set.all()
    projects = Project.objects.filter(team__in=teams)

    if id == 'all':
        logs_list = Logger.objects.filter(
            project__in=projects).filter(published=True).order_by('-date_created')
        context = {
            "projects": projects.order_by('title'),
            "page_title": "Project logs:",
            "userpage": True,
            "loglistpage": True,
            "selected": 'all',
            "welcomemessage": 'Create your first log by clicking on the "New Log" Button !',
        }
    else:
        try:
            id = UUID(id, version=4)
        except ValueError:
            context = {
                "error": "Invalid project ID.",
            }
            return render(request, 'log/list_view.html', context)
        project = projects.filter(id=id)
        if not project.exists():
            context = {
                "error": "You are not a part of this project.",
            }
            return render(request, 'log/list_view.html', context)

        logs_list = Logger.objects.filter(
            project__in=project).filter(published=True).order_by('-date_created')
        context = {
            "projects": projects.order_by('title'),
            "page_title": "Project logs:",
            "userpage": True,
            "loglistpage": True,
            "selected": project[0].id,
            "welcomemessage": 'Create your first log by clicking on the "New Log" Button !',
        }

    paginator = Paginator(logs_list, 10)
    page = request.GET.get('page')
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        logs = paginator.page(1)
    except EmptyPage:
        logs = paginator.page(paginator.num_pages)

    context["logs"] = logs
    context["page"] = page

    return render(request, 'log/list_view.html', context)


@login_required
def logEditView(request, *args, **kwargs):

    logtoview = kwargs.get('pk')

    try:
        logtoview = UUID(str(logtoview))
    except ValueError:
        return HttpResponse("Error: Invalid log ID", status=400)
<<<<<<< HEAD

=======
>>>>>>> upstream/master

    try:
        thelog = Logger.objects.get(id=logtoview)
        password = thelog.password

        BLOCK_SIZE = 32
        encryption_suite = AES.new(password.encode(), AES.MODE_ECB)

        deciphered_text = encryption_suite.decrypt(bytes.fromhex(thelog.note))
        padding = deciphered_text[-1]
        deciphered_text = deciphered_text[:-padding].decode()

        thelog.note = deciphered_text
    except ObjectDoesNotExist:
        return HttpResponse("Error: Invalid log ID", status=400)
    except:
        messages.add_message(request, messages.ERROR,
                             "An Unknown error occurred.")
        return redirect('landing-page')

    if request.method == "POST":
        log_title = request.POST.get('log-title', "")
        log_description = request.POST.get('log-description', "")
        log_content = request.POST.get('log-content', "")

        # changelog = Logger.objects.
        BLOCK_SIZE = 32
        encryption_suite = AES.new(thelog.password.encode(), AES.MODE_ECB)

        cipher_text = encryption_suite.encrypt(
            pad(log_content.encode(), BLOCK_SIZE)).hex()

        thelog.title = log_title
        thelog.short_description = log_description
        thelog.note = cipher_text
        thelog.save()

        messages.add_message(request, messages.SUCCESS,
                             "Log saved successfully.")
        return redirect('log-list')

    context = {
        "log": thelog,
        "files": LogFile.objects.filter(user=request.user),

    }

    return render(request, 'log/log_edit_view.html', context)


@login_required
def recBinView(request):
    if request.method != "GET":
        logs_to_delete = Logger.objects.filter(
            user=request.user).filter(published=False)
        try:
            logs_to_delete.delete()
        except Exception as e:
            messages.add_message(request, messages.ERROR,
                                 f"Could not empty recycle bin. Error: {e}")
        messages.add_message(request, messages.SUCCESS,
                             f"Recycle bin was cleared successfully.")
        return redirect('log-bin')

    else:
        logtodelete = request.GET.get('id', "")

        if logtodelete == "":
            context = {
<<<<<<< HEAD
                "logs": Logger.objects.filter(user=request.user).filter(published=False).order_by('-date_created')
=======
                "page_title": "Recycle Bin",
                "logs": Logger.objects.filter(user=request.user).filter(published=False).order_by('-date_created'),
                "userpage": True,
                "welcomemessage": "Your bin is empty"
>>>>>>> upstream/master
            }
            return render(request, 'log/bin_view.html', context)
        else:
            try:
                logtodelete = UUID(logtodelete)
            except ValueError:
                return HttpResponse("Error: Invalid log ID", status=400)
<<<<<<< HEAD

=======
>>>>>>> upstream/master

            try:
                log = Logger.objects.get(id=logtodelete)
                log.published = True
                log.save()
                messages.add_message(
                    request, messages.SUCCESS, "Log was successfully recovered.")
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


@login_required
def shareController(request):
    if request.method == "GET":
        return HttpResponse("GET request not allowed", status=403)
    if request.method == "POST":
        print(request.POST.dict())
        usernames = request.POST.get('usernames', '')
        logid = request.POST.get('loguuid', '')

        try:
            logtoview = UUID(str(logid))

        except ValueError:
<<<<<<< HEAD
            return JsonResponse({"message":"Log ID Invalid. Please contact Administrator."}, status=400)
=======
            return JsonResponse({"message": "Log ID Invalid. Please contact Administrator."}, status=400)
>>>>>>> upstream/master

        try:
            thelog = Logger.objects.get(id=logtoview)
            usernames = usernames.split(',')

        except ObjectDoesNotExist:
            return JsonResponse({"message": "Log ID Invalid. Please contact Administrator."}, status=400)
        except Exception as ಠ_ಠ:
            print(ಠ_ಠ)
            return JsonResponse({"message": "An unknown error occurred."}, status=400)
        print(usernames)
        if usernames == [""]:
            thelog.access.set([])
<<<<<<< HEAD
            return JsonResponse({"message":"Shared users cleared successfully."})



=======
            return JsonResponse({"message": "Shared users cleared successfully."})

>>>>>>> upstream/master
        doesnotexistlist = []
        existslist = []

        # Remove the @ sign.
        usernames = [x[1:] for x in usernames]

        for users in usernames:
<<<<<<< HEAD

=======
>>>>>>> upstream/master

            try:
                existslist.append(User.objects.get(username=users))

            except ObjectDoesNotExist as ಠ_ಠ:
                doesnotexistlist.append(users)

            except Exception as ಠ_ಠ:
<<<<<<< HEAD
                return JsonResponse({"message":"An unknown error occurred."}, status=400)

=======
                return JsonResponse({"message": "An unknown error occurred."}, status=400)
>>>>>>> upstream/master

        if doesnotexistlist != []:
            doesnotexistlist = ["@" + x for x in doesnotexistlist]

            if len(doesnotexistlist) == 1:

                return JsonResponse({"message": f"{doesnotexistlist[0]} does not exist."}, status=400)
            else:
                return JsonResponse({"message": 'Usernames "' + ', '.join(doesnotexistlist) + '" do not exist.'}, status=400)
<<<<<<< HEAD

=======
>>>>>>> upstream/master

        thelog.access.set(existslist)
    if request.method == "GET":
        pass
    shareurl = reverse('log-detail', args=[logid])
    return JsonResponse({"message": f'Log shared Successfully<br>Link : <a href="{shareurl}">{shareurl}</a>'}, status=200)


@login_required
def mySharesView(request):

    context = {
        "logs": request.user.user_access.all().filter(published=True).order_by('-date_created'),
        "page_title": "Shared with me:",
        "userpage": False,
<<<<<<< HEAD
    }
    return render(request, 'log/list_view.html', context)

=======
        "welcomemessage": 'You don\'t have any shared logs!'
    }
    return render(request, 'log/list_view.html', context)
>>>>>>> upstream/master


def searchResults(request):

    query = request.GET.get('q', '')

    teams = request.user.team_set.all()
    projects = Project.objects.filter(team__in=teams)
    logs = Logger.objects.filter(project__in=projects).filter(Q(title__icontains=query) | Q(short_description__icontains=query)) | (
        Logger.objects.filter(user=request.user)).filter(Q(title__icontains=query) | Q(short_description__icontains=query))
<<<<<<< HEAD

=======
>>>>>>> upstream/master

    context = {
        "logs": logs,
        "page_title": "Search results:",
        "userpage": False,
    }
    return render(request, 'log/list_view.html', context)

<<<<<<< HEAD
=======

>>>>>>> upstream/master
@login_required
def deleteAllLogs(request):
    user = request.user
    logs = Logger.objects.filter(user=request.user, )


def markdownGuide(request):
    try:

        return FileResponse(open(os.path.join(BASE_DIR, 'log', 'markdown-guide.pdf'), 'rb'), content_type='application/pdf')

    except FileNotFoundError:
        raise Http404()
