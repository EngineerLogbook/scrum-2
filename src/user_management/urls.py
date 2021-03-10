from django.urls import path, include
from django.contrib.auth import views as auth_views
from user_management import views as user_views
urlpatterns = [
    # Custom
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),

    path('terms/', user_views.terms, name='terms'),
    path('<uuid:pk>/',
         user_views.UserDetailView.as_view(), name='user-detail'),
    path('privacy/', user_views.privacy, name='privacy'),
    path('disclaimer/', user_views.disclaimer, name='disclaimer'),

    path('contact/', user_views.contact, name='contact'),
    path('ourteam/', user_views.ourteam, name='ourteam'),
    path('404', user_views.notfound, name='notfound'),
    path('faqs/', user_views.faqs, name='faqs'),
    path('aboutus/', user_views.aboutus, name='aboutus'),
    path('feedback/', user_views.feedback, name='feedback'),
    path('terms/', user_views.tac, name='terms'),
    path('privacypolicy/', user_views.privacy, name='privacy-policy'),

    # In Built
    path('login/', user_views.RedirectingLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='user_management/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='user_management/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='user_management/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='user_management/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='user_management/password_reset_complete.html'), name='password_reset_complete'),


    # For ungregisterd users

    path('', user_views.landing_page_view, name='landing-page'),
    path('1/', user_views.landing_page_view_1, name='landing-page-1'),

    # For userlist search

    path('api/user/', user_views.UserAPIView.as_view())
]
