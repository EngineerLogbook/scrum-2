
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@thapar.edu" not in data:   # any check you need
            raise forms.ValidationError("Must be a thapar.edu email address")
        return data

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email', 'class': 'form-control'}),
        max_length=254,
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'First Name', 'class': 'form-control'}),
        max_length=30,
        required=True,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
        max_length=30,
        required=True,
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Username', 'class': 'form-control'}),
        max_length=30,
        required=True,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Phone', 'class': 'form-control'}),
        max_length=30,
        required=True,
    )

    class Meta:
        model = Profile
        fields = ['gender', 'degree', 'field_study',
                  'year_grad', 'phone', 'image']
