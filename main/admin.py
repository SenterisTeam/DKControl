from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import *

admin.site.register(Note)
admin.site.register(StudySession)
admin.site.register(Attending)
admin.site.register(Union)
admin.site.register(Group)
admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(ParentMore)
admin.site.register(StudentMore)
admin.site.register(EmployeeMore)
admin.site.register(Logo)



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ('username',)

    fieldsets = (
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'patronymic', 'username', 'password', 'theme')
        }),
    )


@admin.register(TimetableElem)
class TimetableElemAdmin(admin.ModelAdmin):
    fields = ('begin_time', 'day', 'group')
