from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from main.models import Parent
from main.views.functionsAndClasses.setModel import setModel


@login_required(login_url="/login/")
def get_parent(request, parent):
    parent_model = Parent.objects.get(id=parent)
    if setModel(parent_model, request):
        return redirect('parent', parent)
    return render(request, 'parent.html', {"parent": parent_model})