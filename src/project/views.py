from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import (
    TemplateView,
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project, Team
from log.models import Logger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import JoinTeamForm
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy

class ProjectListView(LoginRequiredMixin,   ListView):
    """
        Lists of Projects in a single view of a Specific Logged IN USER
    """
    model = Project
    template_name = 'project/project_list.html'
    context_object_name = 'projects'
    ordering = ['-title']
    paginate_by = 5

    def test_func(self):
        return True


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'project/project_create.html'
    fields = ['title', 'description']


    def form_valid(self, form):
        self.object = form.save()
        self.object.admin = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class ProjectDetailView(LoginRequiredMixin,  DetailView):
    """
        Details of the Project would have links to Detail Data
    """
    model = Project
    context_object_name = 'project'
    template_name = 'project/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_teams'] = Team.objects.filter(project=self.object)
        return context


class ProjectUpdateView(LoginRequiredMixin,  UpdateView):
    model = Project
    template_name = 'project/project_update.html'


class TeamListView(LoginRequiredMixin,  ListView):
    model = Team
    template_name = 'proeject/team_list.html'
    context_object_name = 'teams'

    def get_queryset(self):
        listOProjects = self.request.user.team_set.all(
        ).values_list('project', flat=True).distinct()
        teams = Team.objects.filter(project_id__in=listOProjects)
        
        return teams



class TeamCreateView(LoginRequiredMixin,  CreateView):
    model = Team
    template_name = 'project/team_create.html'
    fields = ['title', 'project', 'description']

    def form_valid(self, form):
        self.object = form.save()
        self.object.members.add(self.request.user)
        self.object.admin = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class JoinTeamView(LoginRequiredMixin, TemplateView):
    """
        View for Joining Team that has been created
    """
    template_name = 'project/team_join.html'


class TeamDetailView(LoginRequiredMixin,  DetailView):
    """
       Details of specific team in the website
    """
    model = Team
    template_name = 'project/team_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        context['show_token'] = False
        context['members'] = team.members.all()
        context['project'] = team.project
        if self.request.user in team.members.all():
            context['show_token'] = True

        return context


class TeamUpdateView(LoginRequiredMixin,  UpdateView):
    """
        Update The Team Details
    """
    model = Team
    template_name = 'project/team_update.html'


class TeamListAllView(LoginRequiredMixin,  ListView):
    """
    Lists all Teams in the whole website for Instructor's Mostly
    """
    model = Team
    template_name = 'project/team_listall.html'


class ProjectListAllView(LoginRequiredMixin,  ListView):
    """
    This view would list all teams in the whole website (mostly for )

    """
    model = Project
    template_name = 'project/project_listall.html'

@login_required
@require_http_methods(['POST',])
def deleteTeamView(request):
    try:
        pk = request.POST.get('pk', "")
        team = Team.objects.get(id=pk)
        if request.user != team.admin:
            return HttpResponse("You are not authorized to perform this action", status=400)
        team.delete()
        messages.success(request, "Team Deleted Successfully")
        return redirect('team-list')
    except ObjectDoesNotExist:
        return HttpResponse("Bad Request", status=400)
    
    return HttpResponse()


@login_required
def projectListView(request):

    teams = request.user.team_set.all()
    project_list = []

    for project in Project.objects.all():
        try:

            # add member and log count
            project.nooflogs = Logger.objects.filter(project=project).count()
            project.noofteams = project.team_set.all().count()
            print(project.noofteams, project.nooflogs)

            # Limit description length
            if len(project.description) > 130:
                project.description = project.description[:130] + "..."
            project_list.append(project)
        except Exception as e:
            print(e)

    context = {
        "projects": project_list
    }
    return render(request, 'project/projectList.html', context)


@login_required
def projectCreateView(request):
    if request.method == "GET":
        context = {
            "teams": request.user.team_set.all()
        }
        return render(request, 'project/createProject.html', context)

    if request.method == "POST":
        title = request.POST.get('project-title')
        description = request.POST.get('project-description')

        banner = request.POST.get('project-banner')
        print(request.POST.dict())

        print(type(banner))
        print(title, description, banner)
        return render(request, 'project/createProject.html', {})


@login_required
def gettingStartedView(request):
    return render(request, 'project/teampage.html', {})


@login_required
def jointeamview(request):

    if request.method == "POST":
        form = JoinTeamForm(request.POST)
        form_token = request.POST.get('token')
        if form.is_valid():
            t = Team.objects.filter(token=form_token)[0]

            # if t.members :
            #     messages.warning(request, 'You have already been added to team %s', t.title)
            #     return redirect('team-detail', id='title')

            if t:
                t.members.add(request.user)
                t.save()
                context = {
                    "Team": t
                }
                messages.success(request, 'Added to Team ', t.title)
                return render(request, 'project/team_join_confirm.html', context)
            else:

                context = {
                    "form": JoinTeamForm
                }
                messages.info(request, 'Enter key to join your team')
                return render(request, 'project/team_join.html', context)
        else:

            context = {
                "form": JoinTeamForm
            }
            messages.error(request, 'Incorrect token')
            return render(request, 'project/team_join.html', context)
    elif request.method == "GET":

        context = {
            "form": JoinTeamForm
        }
        messages.info(request, 'Enter key to join your team')
        return render(request, 'project/team_join.html', context)
