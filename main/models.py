import datetime as dt
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


# region Models
class Note(models.Model):
    student = models.ForeignKey("Student", verbose_name="Студент", related_name="student", on_delete=models.CASCADE)
    user = models.ForeignKey("User", verbose_name="Пользователь", related_name="user", on_delete=models.CASCADE)
    text = models.TextField("Текст")


class StudySession(models.Model):  # Class Class x
    date = models.DateTimeField("Дата и время начала")
    group = models.ForeignKey("Group", verbose_name="Группа", on_delete=models.CASCADE)
    teacherAttended = models.BooleanField("Педагог был на занятии", default=True, blank=True)
    cancelReason = models.CharField("Причина отмены", max_length=128, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.group.name} [{self.date.strftime('%d.%m.%Y %H:%M:%S')}]"


class Attending(models.Model):
    student = models.ForeignKey("Student", verbose_name="Студент", on_delete=models.CASCADE)
    isAttend = models.BooleanField("Посетил", default=False)
    studySession = models.ForeignKey(StudySession, verbose_name="Занятие", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.last_name} -> {self.studySession.__str__()}"


class Union(models.Model):
    name = models.CharField("Название", max_length=64, default="No name")
    occupationReason = models.CharField("Причина занятости", max_length=128, null=True, blank=True, default=None)

    logo = models.ForeignKey("Logo", verbose_name="Лого", blank=True, null=True,
                             on_delete=models.SET_NULL)  # TODO Под вопросом

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField("Название", max_length=16)
    union = models.ForeignKey(Union, on_delete=models.CASCADE, verbose_name="Объединение", null=True)
    teacher = models.ForeignKey("User", verbose_name="Педагог", on_delete=models.SET_NULL, null=True, blank=True)

    # TODO нужно ли архивировать группы?

    def __str__(self):
        return f"{self.union.name}/{self.name}"


class TimetableElem(models.Model):
    beginTime = models.TimeField("Время начала")
    endTime = models.TimeField("Время конца", blank=True, default="00:00:00")

    DAYS = (
        ('ПН', 'Понедельник'),
        ('ВТ', 'Вторник'),
        ('СР', 'Среда'),
        ('ЧТ', 'Четверг'),
        ('ПТ', 'Пятница'),
        ('СБ', 'Суббота'),
    )
    day = models.CharField('День', max_length=2, choices=DAYS)
    group = models.ForeignKey("Group", verbose_name="Группа", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.endTime = (dt.datetime.combine(dt.date(1, 1, 1), self.beginTime) + dt.timedelta(
            minutes=100)).time()  # С костыля, ША! FullStackOverflow наше всё (работает на божей силе:b)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.day} в {self.beginTime.strftime('%H:%M')}-{self.endTime.strftime('%H:%M')}"


class User(AbstractUser):
    profile_icon = models.ImageField("Фото профиля", upload_to="profile_icon", blank=True, null=True)

    patronymic = models.CharField('Отчество', max_length=16, blank=True, default="")
    birthday = models.DateField('Дата рождения', null=True, blank=True)

    GENDER_CHOICES = (
        ('Женский', 'Женский'),
        ('Мужской', 'Мужской'),
    )
    gender = models.CharField('Пол', max_length=7, choices=GENDER_CHOICES, null=True, blank=True)

    address = models.CharField('Адрес', max_length=128, null=True, blank=True)
    phone = models.IntegerField('Телефон', null=True, blank=True)

    is_archived = models.BooleanField('В архиве', default=False, blank=True)

    class Types(models.TextChoices):
        EMPLOYEE = "Сотрудник", "Сотрудник"
        STUDENT = "Студент", "Студент"
        PARENT = "Родитель", "Родитель"

    base_type = Types.EMPLOYEE

    type = models.CharField("Тип", max_length=50, choices=Types.choices, default=base_type)

    THEME_CHOICES = (
        ('theme_light', 'Светлая тема'),
        ('theme_dark', 'Тёмная тема'),
    )

    theme = models.CharField("Тема оформления", max_length=64, choices=THEME_CHOICES, default=THEME_CHOICES[0][0])

    def save(self, *args, **kwargs):
        if not self.id and not self.type:
            self.type = self.base_type

        save = super().save(*args, **kwargs)

        if not self.username and self.id is not None:
            self.username = f'user_{self.id}'
            super().save(*args, **kwargs)

        if self.type == "Сотрудник":
            EmployeeMore.objects.get_or_create(user=self)
        elif self.type == "Студент":
            StudentMore.objects.get_or_create(user=self)
        elif self.type == "Родитель":
            ParentMore.objects.get_or_create(user=self)

        return save

    def __str__(self):
        return f"{self.last_name} {self.first_name}  {self.patronymic}"

    class Meta:
        permissions = [
            ("has_groups", "Имеет группы"),
            ("edit_any_studySession", "Редактирует любые занятия"),
            ("cancel_studySession", "Отменяет занятия"),
        ]

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"


class EmployeeMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    union = models.ForeignKey(Union, verbose_name="Объединение", on_delete=models.SET_NULL, blank=True, null=True)


class StudentMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    school = models.CharField('Школа', max_length=32, blank=True, null=True)
    grade = models.CharField('Класс', max_length=3, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="students", verbose_name="Группы", blank=True)
    parents = models.ManyToManyField("Parent", related_name="childs", verbose_name="Родители", blank=True)


class ParentMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class EmployeeManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.EMPLOYEE)


class Employee(User):
    base_type = User.Types.EMPLOYEE
    objects = EmployeeManager()

    @property
    def more(self):
        return self.employeemore

    class Meta:
        proxy = True


class StudentManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.STUDENT)


class Student(User):
    base_type = User.Types.STUDENT
    objects = StudentManager()

    @property
    def more(self):
        return self.studentmore

    class Meta:
        proxy = True


class ParentManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.PARENT)


class Parent(User):
    base_type = User.Types.PARENT
    objects = ParentManager()

    @property
    def more(self):
        return self.parentmore

    class Meta:
        proxy = True


# endregion

# region Other models
class Logo(models.Model):
    name = models.CharField("Название", max_length=16)
    link = models.ImageField("Иконка", upload_to="logo")

    def __str__(self):
        return self.name
# endregion
