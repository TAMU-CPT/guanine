from django.contrib.auth.models import User, Group
from rest_framework import serializers
from base.models import Course, Assessment, Result, Student

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')

class AssessmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assessment
        fields = ('description', 'end_date', 'title', 'id', 'course', 'start_date')

class ResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Result
        fields = ('points_possible', 'points_earned', 'submitted', 'student', 'assessment', 'id')

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('email', 'id', 'name')

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    professor = UserSerializer(read_only=True, many=True)
    students = StudentSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ('description', 'id', 'name', 'students', 'professor')#, 'students', 'professor')
