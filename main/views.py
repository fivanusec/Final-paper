import base64
import pandas as pd

from os import path, walk, remove
from io import BytesIO
from cv2 import imread, imwrite

from PIL import Image
from uuid import uuid4
from deepface import DeepFace

from django.conf import settings
from django.shortcuts import render, redirect

from attendance.models import Attendance
from main.utils import DuplicateRemover, TokenHandler
from students.models import Students


def empty_media():
    for root, dirs, files in walk(settings.MEDIA_ROOT):
        for file in files:
            remove(path.join(root, file))


def home(request):
    response = {}
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        empty_media()
        image_b64 = str(request.POST.get('img'))
        format, imgstr = image_b64.split(';base64,')
        ext = format.split('/')[-1]
        img = Image.open(
            BytesIO(base64.decodebytes(bytes(str(imgstr), "utf-8"))))
        save_path = str(settings.MEDIA_ROOT + f"{uuid4()}.{ext}")
        img.save(save_path)
        result = DeepFace.find(
            imread(save_path),
            db_path=settings.REF_ROOT,
            detector_backend="mtcnn",
            model_name="ArcFace",
        )

        if not result.empty:
            data = pd.DataFrame(result)
            imwrite(
                filename=settings.REF_ROOT +
                str(path.split(path.dirname(data["identity"][0]))[-1]) + "/" +
                str(uuid4()) + str(path.splitext(save_path)[-1]),
                img=imread(save_path),
            )
            try:
                student_data = path.split(path.dirname(
                    data["identity"][0]))[-1]
                student_data = student_data.split()
                student = Students.objects.filter(
                    first_name=student_data[0],
                    last_name=student_data[1]).first()
                attendance = Attendance.objects.filter(
                    student=student.id, confirmed=False,
                    recognition=False).first()
                if attendance:
                    attendance.recognition = True
                    attendance.save()
                duplicate = DuplicateRemover(
                    settings.REF_ROOT + f"{student_data[0]} {student_data[1]}")
                duplicate.find_duplicates()
            except Students.DoesNotExist:
                pass
        response = {
            "detected": {
                "name": student.first_name,
                "last_name": student.last_name
            },
        } if student else {
            "error": "Student was not recognized"
        }
    return render(request, 'main/home.html', {
        'title': "Test",
        'response': response
    })
