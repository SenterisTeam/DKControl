from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from main.models import Group, StudySession, Union, Student, Attending
from main.views.charts import get_attending_stats
from main.views.users_views import set_model


@login_required(login_url="/login/")
def main(request):
    students = Student.objects.all()[:20]
    # region students attending
    if date.today().month >= 9:
        edit_year = 0
    else:
        edit_year = 1

    startday = date(date.today().year - edit_year, 9, 1)
    period_end = startday + relativedelta(months=10)
    attendings = [round(get_attending_stats(startday, period_end, None, None, student.id)[0] * 100) for student in students]
    # endregion
    return render(request, 'unions.html', {'students': students, 'attendings': attendings, 'unions': Union.objects.all()})


def get_session(request, session):
    session = StudySession.objects.get(id=session)
    set_model(session, request)
    return render(request, 'study_session.html', {'session': session})


@login_required(login_url="/login/")
def get_union(request, union):
    union = Union.objects.get(id=union)
    set_model(union, request)
    return render(request, 'union.html', {"union": union})


@login_required(login_url="/login/")
def get_group(request, group):
    group = Group.objects.get(id=group)
    set_model(group, request)
    timetable = {
        "ПН": {},
        "ВТ": {},
        "СР": {},
        "ЧТ": {},
        "ПТ": {},
        "СБ": {},
    }

    for time in group.timetableelem_set.all():
        timetable[time.day] = {"time": f"{time.begin_time.strftime('%H:%M')}-{time.end_time.strftime('%H:%M')}"}

    # region students attending
    if date.today().month >= 9: edit_year = 0
    else: edit_year = 1

    startday = date(date.today().year - edit_year, 9, 1)

    period_end = startday + relativedelta(months=10)

    attendings = [round(get_attending_stats(startday, period_end, None, group.id, student.id)[0] * 100) for i, student in enumerate(group.students.all())]
    # endregion

    return render(request, 'group.html', {"group": group, "timetable": timetable, "attendings": attendings})


def set_attending(request, attending):
    attending = Attending.objects.get(id=attending)
    attending.is_attend = bool(request.GET.get("status"))
    attending.save()
    return JsonResponse({})
