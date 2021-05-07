from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_nested.routers import NestedSimpleRouter

from api.views.search import SearchView
from api.views.views import *

router = DefaultRouter()

router.register(r'users', UserView, basename='User')
router.register(r'notes', NoteView, basename='Note')
router.register(r'unions', UnionView, basename='Union')
router.register(r'groups', GroupView, basename='Group')
router.register(r'timetable-elems', TimetableElemView, basename='Timetable Elem')
router.register(r'employee-more', EmployeeMoreView, basename='Employee More')
router.register(r'students-more', StudentMoreView, basename='Student More')
router.register(r'parents-more', ParentMoreView, basename='Parent More')
router.register(r'logos', LogoView, basename='Logo')
router.register(r'students', StudentView, basename='Student')
router.register(r'parents', ParentView, basename='Parent')
router.register(r'employees', EmployeeView, basename='Employee')

router.APIRootView = OverviewView

groups_router = NestedSimpleRouter(router, r'groups', lookup='group')
groups_router.register(r'sessions', GroupSessionsView, basename='group-sessions')

session_router = NestedSimpleRouter(groups_router, r'sessions', lookup='session')
session_router.register(r'attendings', SessionAttendingsView, basename='session-attendings')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(groups_router.urls)),
    path('', include(session_router.urls)),

    path('search/', SearchView.as_view(), name='search'),

    path('auth/', include('rest_framework.urls')),
    path('token-auth/', obtain_jwt_token)
]
