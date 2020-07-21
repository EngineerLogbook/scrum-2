from django import forms
from .models import Team, Project


class JoinTeamForm(forms.ModelForm):
    token = forms.UUIDField(
        widget=forms.TextInput(
            attrs={'placeholder': 'token', 'class': 'form-control'}),
    )

    class Meta:
        model = Team
        fields = ['token']
