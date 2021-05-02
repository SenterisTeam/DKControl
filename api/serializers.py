from rest_framework import serializers

from main.models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        print(validated_data['type'])
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            type=validated_data['type'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            patronymic=validated_data['patronymic'],
        )

        return user

    class Meta:
        model = User
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class StudySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySession
        fields = '__all__'


class AttendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attending
        fields = '__all__'


class UnionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Union
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class TimetableElemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetableElem
        fields = '__all__'


class EmployeeMoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMore
        fields = '__all__'


class StudentMoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMore
        fields = '__all__'


class ParentMoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentMore
        fields = '__all__'


class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    more = StudentMoreSerializer()

    class Meta:
        model = Student
        fields = '__all__'


class ParentSerializer(serializers.ModelSerializer):
    more = ParentMoreSerializer()

    class Meta:
        model = Parent
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    more = EmployeeMoreSerializer()

    class Meta:
        model = Employee
        fields = '__all__'
