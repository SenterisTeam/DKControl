from rest_framework import permissions, serializers
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.routers import APIRootView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from main.models import *
from api.serializers import *


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request: Request, *args, **kwargs):
        """
        If provided 'pk' is "me" then return the current user.
        """
        if kwargs.get('pk') == 'me':
            return Response(self.get_serializer(request.user).data)
        return super().retrieve(request, args, kwargs)


class NoteView(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


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


class GroupSessionsView(ModelViewSet):
    serializer_class = StudySessionSerializer

    def get_queryset(self):
        return StudySession.objects.filter(group=self.kwargs['group_pk'])


class SessionAttendingsView(ModelViewSet):
    serializer_class = AttendingSerializer

    def get_queryset(self):
        return Attending.objects.filter(study_session=self.kwargs['session_pk'], study_session__group=self.kwargs['group_pk'])


class OverviewView(APIRootView):
    pass
