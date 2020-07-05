from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .models import History
# Create your views here.



def userHistoryView(request):

    context = {
        "history":request.user.history_set.all().order_by('-date_created'),
        "page_title":"My History : ",
        "userpage":False,
    }
    return render(request, 'history/user_history.html', context)
    

def completeHistoryView(request):

    history_list = []
    user_teams = request.user.team_set.all()
    for team in user_teams:
        [history_list.append(te.id) for te in team.history_set.all()]
        for project in Project.objects.all():
            [history_list.append(te.id) for te in project.history_set.all()]

    [history_list.append(te.id) for te in request.user.history_set.all()]

    print(history_list)

    context = {
        "history":History.objects.filter(id__in=history_list).order_by('-date_created'),
        "page_title":"Complete History : ",
        "userpage":False,
    }
    return render(request, 'history/complete_history.html', context)
    