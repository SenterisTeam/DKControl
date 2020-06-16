from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from main.models import User
from main.views.functionsAndClasses.setModel import setModel


@login_required(login_url="/login/")
def getUser(request, user):
    user_model = User.objects.get(id=user)
    if setModel(user_model, request):
        return redirect('user', user)
    return render(request, 'user.html', {"user": user_model})