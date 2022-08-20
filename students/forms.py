from django import forms
from .models import Students


class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['first_name', 'last_name', 'email', 'year', 'field_of_study']
