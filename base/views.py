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

    def get_queryset(self):
        if not self.request.user.is_anonymous():
            return Course.objects.filter(professor = self.request.user)
        # for testing
        else:
            return Course.objects.all()

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
