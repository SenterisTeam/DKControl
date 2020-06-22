import threading
import time
from datetime import datetime
import pytz
from django.utils.timezone import now
import locale
from DKControl import settings
from main.models import StudySession, Group, Attending

WAIT_SECONDS = 1

user_timezone = pytz.timezone(settings.TIME_ZONE)
now().astimezone(user_timezone)


def session_creator():
    for group in Group.objects.all():
        for timetable_elem in group.timetableelem_set.all():
            if datetime.now().strftime("%a").upper() == timetable_elem.day:
                if timetable_elem.beginTime >= datetime.now().time():
                    continue
                if not [None for session in group.studysession_set.all()
                        if session.date.strftime("%a").upper() == timetable_elem.day and session.date.date() == now().date() and session.date.time() > datetime.now().time()]:

                    datetime_begin = now()
                    datetime_begin = datetime_begin.replace(hour=timetable_elem.beginTime.hour, minute=timetable_elem.beginTime.minute, second=0)
                    new_session = StudySession(date=datetime_begin, group=group)
                    new_session.save()
                    for student in group.students.all():
                        new_attending = Attending(student=student, studySession=new_session)
                        new_attending.save()

                    print(f"[{datetime.now()}] New session {new_session}")

    thread = threading.Timer(WAIT_SECONDS, session_creator)
    thread.daemon = True
    thread.start()
