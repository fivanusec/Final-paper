from django.db import models
from django.utils.timezone import now

from students.models import Students


class Attendance(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, null=False)
    confirmed = models.BooleanField(null=True, default=False)
    recognition = models.BooleanField(null=True, default=False)
    attendance_date = models.DateTimeField(default=now)