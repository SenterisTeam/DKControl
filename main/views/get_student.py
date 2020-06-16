from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from main.models import Student
from main.views.functionsAndClasses.setModel import setModel


@login_required(login_url="/login/")
def get_student(request, student):
    student_model = Student.objects.get(id=student)
    if setModel(student_model, request):
        return redirect('student', student)
    return render(request, 'student.html', {"student": student_model})