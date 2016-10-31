from rest_framework import viewsets, filters
from django.contrib.auth.models import User, Group
from base.serializers import UserSerializer, GroupSerializer, CourseSerializer, AssessmentSerializer, ResultSerializer, StudentSerializer
from base.models import Course, Assessment, Result, Student

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('name',)

    def perform_create(self, serializer):
        """
        Save creator of Course as logged in user on create.
        """
        serializer.save(professor=[self.request.user])

    def get_queryset(self):
        if not self.request.user.is_anonymous():
            return Course.objects.filter(professor = self.request.user)
        else:
            return []

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('course',)
    ordering_fields = ('date',)

    def get_queryset(self):
        if not self.request.user.is_anonymous():
            return Assessment.objects.filter(course__professor=self.request.user)
        else:
            return []

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all().order_by('-submitted')
    serializer_class = ResultSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('student', 'assessment__course')
    ordering_fields = ('assessment__title',)

    def get_queryset(self):
        if not self.request.user.is_anonymous():
            return Result.objects.filter(assessment__course__professor=self.request.user)
        else:
            return []

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('email',)
