from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import Students
from .forms import StudentForm


def create_students(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return redirect("/students")
    else:
        form = StudentForm()
    context = {
        'title': "Create student",
        'form': form
    }
    return render(request, 'students/create_student.html', context)


def update_student(request, id):
    student = get_object_or_404(Students, id=id)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f'Student updated successfully!')
            return redirect("/students")
    return render(request, 'students/update-student.html', {'form': form})


def delete_student(request, id):
    student = get_object_or_404(Students, id=id)
    if request.method == 'POST':
        student.delete()
        return redirect('/students')
    return render(request, 'students/delete_student.html', {})


def students(request):
    data = Students.objects.all()
    page_num = request.GET.get('page', 1)
    paginator = Paginator(data, 10)
    
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'title': "Students",
        'data': page_obj
    }
    return render(request, 'students/students.html', context=context)
