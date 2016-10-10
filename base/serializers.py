from django.contrib.auth.models import User, Group
from rest_framework import serializers
from base.models import Course, Assessment, Class, Student, Result

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups',)

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('professor', 'description', 'id', 'name')

class AssessmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assessment
        fields = ('classtime', 'description', 'end_date', 'title', 'id', 'start_date')

class ClassSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Class
        fields = ('description', 'end_date', 'students', 'id', 'course', 'start_date')

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'email')

class ResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Result
        fields = ('points_possible', 'points_earned', 'submitted', 'student', 'assessment', 'id')
