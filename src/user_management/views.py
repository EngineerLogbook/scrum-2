from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profile
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

class RedirectingLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'user_management/login.html'

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                f'Account "{ username }" has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
   
    return render(request, 'user_management/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'user_management/profile_edit.html', context)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'user_management/profile.html'
    context_object_name = 'profile'


@login_required
def contact(request):
    return render(request, 'user_management/contact.html')


@login_required
def privacy(request):
    return render(request, 'user_management/privacy.html')

def terms(request):
    return render(request, 'user_management/terms.html')

def disclaimer(request):
    return render(request, 'user_management/disclaimer.html')


def landing_page_view(request):
    return render(request, 'user_management/landing.html', context={})


def ourteam(request):
    return render(request, 'user_management/ourteam.html')


def notfound(request):
    return render(request, 'common/404.html')


@login_required
def faqs(request):
    return render(request, 'user_management/faqs.html')

@login_required
def terms(request):
    return render(request, 'user_management/terms.html')

@login_required
def aboutus(request):
    return render(request, 'user_management/about.html')

@login_required
def feedback(request):
    return render(request, 'user_management/feedback.html')


@login_required
def tac(request):
    return render(request, 'common/404.html')
