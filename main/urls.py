from django.urls import path

from main.views.api.deploy import deploy
from main.views.charts import chart_get
from main.views.objects_views import main, set_attending, get_group, get_session, get_union
from main.views.users_views import login, logout, theme, get_student, get_parent, get_user, new_student, new_parent, \
    remove_user, archive_user

urlpatterns = [
    path("", main, name="main"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("theme/", theme, name="theme"),
    path("chart/<str:chart_type>/", chart_get, name="chart"),
    path("students/<int:student>/", get_student, name="student"),
    path("groups/<int:group>/", get_group, name="group"),
    path("parents/<int:parent>/", get_parent, name="parent"),
    path("users/<int:user>/", get_user, name="user"),
    path("sessions/<int:session>/", get_session, name="session"),
    path("attendings/<int:attending>/", set_attending, name="attending"),
    path("unions/<int:union>/", get_union, name='union'),
    path("new/student/", new_student, name="new_student"),
    path("new/parent/", new_parent, name="new_parent"),
    path("students/<int:user>/remove/", remove_user, name="remove_student"),
    path("parents/<int:user>/remove/", remove_user, name="remove_parent"),
    path("students/<int:user>/archive/", archive_user, name="archive_student"),
    path("parents/<int:user>/archive/", archive_user, name="archive_parent"),
    path("api/deploy/", deploy, name="deploy"),
]
