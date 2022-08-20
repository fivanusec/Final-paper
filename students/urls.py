from django.urls import path
from . import views

urlpatterns = [
    path('', views.students, name="Students"),
    path('create-student/', views.create_students, name="Create students"),
    path('update-student/<int:id>', views.update_student, name="Update student"),
    path('delete-student/<int:id>', views.delete_student, name="Delete student")
]
