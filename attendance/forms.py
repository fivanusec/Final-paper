from django import forms
from .models import Attendance


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'attendance_date']


class UpdateAttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = ['subject', 'confirmed']