from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from main.models import Attending, StudySession, Student


@login_required(login_url="/login/")
def chart_get(request, chart_type):
    req = RequestedData(request)

    if chart_type == 'attendingStats' and req.unit == 'days':
        days, results = get_attending(req, req.days)

        return JsonResponse({
            "region": [d.day for d in days],
            "value": [int(round(result * 100)) for result in results]
        })

    if chart_type == 'attendingStats' and req.unit == 'months':
        if date.today().month >= 9:
            edit_year = 0
        else:
            edit_year = 1
        startday = date(date.today().year - edit_year, 9, 1)

        periods_start = [startday + relativedelta(months=s) for s in range(9)]  # Get dates all month
        periods_end = [startday + relativedelta(months=s + 1) for s in range(9)]  # Get dates end all month

        if req.user is None:
            results = [get_attending_stats(periods_start[i], periods_end[i], req.union, req.group, req.student) for i in
                       range(9)]
        else:
            results = [get_attending_teacher_stats(periods_start[i], periods_end[i], req.user) for i in range(9)]

        return JsonResponse({
            "region": ["Сентябрь", "Октябрь", "Ноябрь", "Декабрь", "Январь", "Февраль", "Март", "Апрель", "Май"],
            "value": [int(round(result[0] * 100)) for result in results]
        })


def get_attending(req, daysQuantity):
    startday = date.today() - timedelta(days=daysQuantity - 1)
    days = [startday + timedelta(days=s) for s in range(daysQuantity)]

    results = list()
    if req.user is None:
        for i in range(daysQuantity):
            results.append(get_attending_stats(days[i], days[i], req.union, req.group, req.student)[0])
    else:
        for i in range(daysQuantity):
            results.append(get_attending_teacher_stats(days[i], days[i], req.user)[0])

    i = 0
    for ii in range(daysQuantity):
        if results[i] == 0.001:
            days.pop(i)
            results.pop(i)
        else:
            i += 1

    return days, results


def get_attending_stats(periodStart, periodEnd, union, group, student):
    allAttendings = [a
                     for a in Attending.objects.all()
                     if periodStart <= a.study_session.date.date() <= periodEnd
                     and (union is None or a.study_session.group.union.id == int(union))
                     and (group is None or a.study_session.group.id == int(group))
                     and (student is None or a.student.id == int(student))
                     ]

    attendedAttendings = [a
                          for a in allAttendings
                          if a.is_attend == True
                          ]

    if len(allAttendings) == 0:
        allAttendings = 1000
        attendedAttendings = 1
    else:
        allAttendings = len(allAttendings)
        attendedAttendings = len(attendedAttendings)
    return attendedAttendings / allAttendings, attendedAttendings, allAttendings


def get_attending_teacher_stats(periodStart, periodEnd, user):
    allAttendings = [ss
                     for ss in StudySession.objects.all()
                     if periodStart <= ss.date.date() <= periodEnd
                     ]

    attendedAttendings = [ss
                          for ss in allAttendings
                          if ss.teacher_attended == True
                          ]

    if len(allAttendings) == 0:
        allAttendings = 1;
    else:
        allAttendings = len(allAttendings)
    return len(attendedAttendings) / allAttendings, len(attendedAttendings), allAttendings


def get_gender_stats(union, group, user):
    allStudents = get_all_students(union, group, user)
    maleStudents = [m
                    for m in allStudents
                    if m.gender == "Мужской"
                    ]

    return len(maleStudents) / len(allStudents), len(maleStudents), len(allStudents)


def get_age_stats(min, max, union, group, user):
    allStudents = get_all_students(union, group, user)
    chosenStudents = [m
                      for m in allStudents
                      if min <= m.age <= max
                      ]

    return len(chosenStudents) / len(allStudents), len(chosenStudents), len(allStudents)


def get_all_students(union, group, user):
    result = list()
    for s in Student.objects.all():
        for g in s.groups.all():
            if (union is None or g.union.id == int(union)) \
                    and (group is None or g.id == int(group)) \
                    and (user is None or s.groups == int(user)):
                result.append(s)

    return result


class RequestedData:
    days = None
    unit = None
    periodStart = None
    periodEnd = None
    union = None
    group = None
    student = None
    user = None
    min = None
    max = None

    def __init__(self, request):
        self.days = request.GET.get('days', 30)
        self.unit = request.GET.get('unit', 'days')
        period_start = request.GET.get('ps', None)
        period_end = request.GET.get('pe', None)
        union = request.GET.get('un', None)
        group = request.GET.get('g', None)
        student = request.GET.get('s', None)
        user = request.GET.get('us', None)
        min = request.GET.get('min', 0)
        max = request.GET.get('max', 100)

        if union is not None: self.union = int(union)
        if group is not None: self.group = int(group)
        if student is not None: self.student = int(student)
        if user is not None: self.user = int(user)
        self.min = int(min)
        self.max = int(max)

        if period_start is not None: self.periodStart = date.strftime(period_start, '%Y-%m-%d')
        if period_end is not None: self.periodEnd = date.strftime(period_end, '%Y-%m-%d')
