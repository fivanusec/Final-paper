from django.urls import path

from . import views

urlpatterns = [
    path('', views.attendance, name='Attendance'),
    path('create-attendance/',
         views.create_attendance,
         name="Create attendance"),
    path('update-attendance/<int:id>',
         views.edit_attendance,
         name="update attendance")
]
