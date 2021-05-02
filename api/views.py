from rest_framework import permissions, serializers
from rest_framework.routers import APIRootView
from rest_framework.viewsets import ModelViewSet, ViewSet

from main.models import *
from api.serializers import *


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class NoteView(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class StudySessionView(ModelViewSet):
    queryset = StudySession.objects.all()
    serializer_class = StudySessionSerializer


class AttendingView(ModelViewSet):
    queryset = Attending.objects.all()
    serializer_class = AttendingSerializer


class UnionView(ModelViewSet):
    queryset = Union.objects.all()
    serializer_class = UnionSerializer


class GroupView(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TimetableElemView(ModelViewSet):
    queryset = TimetableElem.objects.all()
    serializer_class = TimetableElemSerializer


class EmployeeMoreView(ModelViewSet):
    queryset = EmployeeMore.objects.all()
    serializer_class = EmployeeMoreSerializer


class StudentMoreView(ModelViewSet):
    queryset = StudentMore.objects.all()
    serializer_class = StudentMoreSerializer


class ParentMoreView(ModelViewSet):
    queryset = ParentMore.objects.all()
    serializer_class = ParentMoreSerializer


class LogoView(ModelViewSet):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer


class StudentView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ParentView(ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer


class EmployeeView(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class OverviewView(APIRootView):
    pass
