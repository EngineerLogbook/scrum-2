from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profile
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework import filters
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from .models import Phase, Member


class RedirectingLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'user_management/login.html'


class UserAPIView(generics.ListCreateAPIView):
    search_fields = ['username']
    filter_backends = (filters.SearchFilter,)
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


def register(request):
    if request.user.is_authenticated:
        return redirect('log-list')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.info(
                request,
                f'Please confirm your email address to complete the registration')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'user_management/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(
            request,
            f'Thank you for your email confirmation.')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


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
    return render(request, 'pages/landing.html', context={})


def ourteam(request):
    teams = Phase.objects.all()
    members = Member.objects.all()

    context = {
        "teams": teams,
        "members": members
    }
    return render(request, 'pages/ourteam.html', context)


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
