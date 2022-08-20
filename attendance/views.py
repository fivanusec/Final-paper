from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from uuid import uuid4
from .forms import AttendanceForm, UpdateAttendanceForm
from .models import Attendance
from main.utils import TokenHandler
from datetime import datetime


def edit_attendance(request, id):
    attendance = Attendance.objects.filter(id=id).first()
    form = UpdateAttendanceForm(request.POST or None, instance=attendance)
    if form.is_valid():
        form.save()
        messages.success(request, f'Attendance updated successfully!')
        return redirect("/attendance")
    return render(request, 'attendance/update_attendance.html', {'form': form})


def create_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("/attendance")
    else:
        form = AttendanceForm()
    return render(request, 'attendance/create_attendance.html', {'form': form})


def attendance(request):
    data = Attendance.objects.all()
    page_num = request.GET.get('page', 1)
    paginator = Paginator(data, 10)
    stats_curr = []
    stats_last = []
    month_nums = [x for x in range(1, 13)]
    stats_all = []

    try:
        for stat in data.filter(recognition=True, confirmed=True):
            if str(datetime.now().month) in str(stat.attendance_date) and str(
                    datetime.now().year) in str(stat.attendance_date):
                stats_curr.append(stat)
            if str(datetime.now().month - 1) in str(
                    stat.attendance_date) and str(datetime.now().year) in str(
                        stat.attendance_date):
                stats_last.append(stat)

        for month in month_nums:
            stats_all.append(
                data.filter(recognition=True,
                            confirmed=True,
                            attendance_date__month=str(month)).count())
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request, 'attendance/attendance.html', {
            "data": page_obj,
            'stats': {
                'month': [len(stats_curr), len(stats_last)],
                'all': stats_all,
            }
        })
