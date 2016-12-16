from django.contrib.auth.models import User, Group
from rest_framework import serializers
from base.models import Course, Assessment, Result, Student

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        write_only_fields = ('password',)

class LiteAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ('description', 'end_date', 'title', 'id', 'course', 'start_date')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('email', 'id', 'name')

class ResultLiteSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = Result
        fields = ('points_possible', 'points_earned', 'submitted', 'student', 'assessment', 'id')

class ResultSerializer(serializers.ModelSerializer):
    assessment = LiteAssessmentSerializer(read_only=True)
    class Meta:
        model = Result
        fields = ('points_possible', 'points_earned', 'submitted', 'student', 'assessment', 'id')

class LiteCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('description', 'id', 'name', 'students')

class AssessmentSerializer(serializers.ModelSerializer):
    result_set = ResultLiteSerializer(many=True, read_only=True)
    course = LiteCourseSerializer(read_only=True)

    class Meta:
        model = Assessment
        fields = ('description', 'end_date', 'title', 'id', 'course', 'start_date', 'result_set')

class CourseSerializer(serializers.ModelSerializer):
    professor = UserSerializer(read_only=True, many=True)
    students = StudentSerializer(many=True)
    assessment_set = AssessmentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('description', 'id', 'name', 'students', 'professor', 'start_date', 'end_date', 'assessment_set')

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
