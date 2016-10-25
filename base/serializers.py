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
    students = StudentSerializer(many=True)

    class Meta:
        model = Course
        fields = ('description', 'id', 'name', 'students', 'professor', 'start_date', 'end_date')

    def create(self, validated_data):
        # List of students
        students = []
        # We get in validated data matching our serializer so safe to work with
        for user in validated_data['students']:
            # Get or create on every passed student
            student, _ = Student.objects.get_or_create(
                name=user['name'],
                email=user['email'],
            )
            # Converting them to a list of Student objects
            students.append(student)

        # We grab the professor list
        profs = validated_data['professor']
        # And remove both lists since we can't initialize with a M2M
        del validated_data['professor']
        del validated_data['students']

        # Now we're safe to create the course
        course = Course.objects.create(**validated_data)
        # And specify the prof/students.
        course.professor = profs
        course.students = students
        return course
