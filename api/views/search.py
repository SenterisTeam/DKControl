import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import *
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.exceptions import ParseError

from rest_framework.views import APIView
from rest_framework.response import Response

from main.models import *


class SearchView(APIView):
    """
    View to search in the system.
    """

    def get(self, request):
        """
        Return a search result
        """
        query = request.GET.get('q')
        extend = request.GET.get('extend')
        if query is None:
            raise ParseError("Не указан запрос (?q=")
        elif len(query) == 0 and extend is None:
            return Response({"results": {"additions": {
                "name": "Дополнительно",
                "results": [
                    {"title": f"Расширинный поиск", "description": 'Поиск с фильтрами', "url": "/search"}]
            }}})
        else:
            query = query.split()

            students = Student.objects.annotate(
                full_name=Concat('last_name', V(' '), 'first_name', V(' '), 'patronymic')) \
                .filter(Q(is_archived=False))
            teachers = Employee.objects.annotate(
                full_name=Concat('last_name', V(' '), 'first_name', V(' '), 'patronymic')) \
                .filter(Q(is_archived=False))
            # .filter(Q(groups__name='Педагог', is_archived=False))
            parents = Parent.objects.annotate(full_name=Concat('last_name', V(' '), 'first_name', V(' '), 'patronymic'))

            groups = Group.objects.annotate(full_name=Concat('union__name', V(' '), 'name'))
            study_sessions = StudySession.objects.all()

            if extend is not None:
                filters = request.GET.get('filters')
                if filters is not None:
                    filters = filters.split(',')
                    filters = list({'students', 'teachers', 'parents', 'groups', 'sessions'} - set(filters))
                    if len(filters) != 5 or len(query) == 0:
                        if "students" in filters:
                            students = students.none()
                        if "teachers" in filters:
                            teachers = teachers.none()
                        if "parents" in filters:
                            parents = parents.none()
                        if "groups" in filters:
                            groups = groups.none()
                        if "sessions" in filters:
                            study_sessions = study_sessions.none()

                age_range = request.GET.get('age')
                if age_range is not None:
                    age_range = age_range.split('-')
                    for i, age in enumerate(age_range):
                        age_range[i] = date.today() - relativedelta(years=int(age))
                    students = students.filter(birthday__range=[age_range[1], age_range[0]])

                date_start = request.GET.get('start')
                date_end = request.GET.get('end')
                if date_start is not None and date_end is not None:
                    if date_start == '': date_start = datetime.datetime(2000, 1, 1)
                    if date_end == '': date_end = datetime.datetime.now()
                    study_sessions = study_sessions.filter(date__range=[date_start, date_end])

            for query in query:
                students = students.filter(Q(full_name__icontains=query))
                teachers = teachers.filter(Q(full_name__icontains=query))
                parents = parents.filter(Q(full_name__icontains=query))
                groups = groups.filter(Q(full_name__icontains=query))
                study_sessions = [s for s in study_sessions if
                                  query in s.date.strftime("%d.%m.%Y %H:%M:%S") or query in s.group.__str__()]

            return Response({"results": {
                **({"students": {
                    "name": "Ученики",
                    "results": [{"title": f"{s.last_name} {s.first_name} {s.patronymic}",
                                 "description": f"{', '.join([g.__str__() for g in s.groups.all()])}",
                                 "url": f"/students/{s.id}",
                                 "extend": [{"name": g.__str__(), "url": f"/groups/{g.id}"} for g in
                                            s.more.groups.all()]}
                                for s in students],
                }} if len(students) > 0 else {}),
                **({"teachers": {
                    "name": "Педагоги",
                    "results": [
                        {"title": f"{s.last_name} {s.first_name} {s.patronymic}",
                         "description": f"{', '.join([g.__str__() for g in s.group_set.all()])}",
                         "url": f"/employees/{s.id}",
                         "extend": [{"name": g.__str__(), "url": f"/groups/{g.id}"} for g in s.group_set.all()]} for s
                        in
                        teachers]
                }} if len(teachers) > 0 else {}),
                **({"parents": {
                    "name": "Родители",
                    "results": [
                        {"title": f"{s.last_name} {s.first_name} {s.patronymic}",
                         "description": f"{', '.join([c.user.__str__() for c in s.childs.all()])}",
                         "url": f"/parents/{s.id}",
                         "extend": [{"name": c.user.__str__(), "url": f"/students/{c.user.id}"} for c in
                                    s.childs.all()]}
                        for s in parents]
                }} if len(parents) > 0 else {}),
                **({"groups": {
                    "name": "Группы",
                    "results": [
                        {"title": f"{s.name} {s.union.name}",
                         "description": f"{', '.join([t.__str__() for t in s.timetableelem_set.all()])}",
                         "url": f"/groups/{s.id}/",
                         "extend": [{"name": g.__str__(), "url": f"/students/{g.id}"} for g in s.students.all()]} for s
                        in
                        groups]
                }} if len(groups) > 0 else {}),
                **({"sessions": {
                    "name": "Занятия",
                    "results": [
                        {"title": f"{s.group} {s.date.strftime('%d.%m.%Y %H:%M:%S')}",
                         "description": f"{s.group}",
                         "url": f"/groups/{s.group.id}/sessions/{s.id}",
                         "extend": [{"name": s.group.__str__(), "url": f"/groups/{s.group.id}/"}]} for s in study_sessions]
                }} if len(study_sessions) > 0 else {}),
                **({"additions": {
                    "name": "Дополнительно",
                    "results": [
                        {"title": f"Расширинный поиск", "description": 'Поиск с фильтрами', "url": "/search"}]
                }} if extend is None else {}),
            }})
