from rest_framework import viewsets, filters, permissions, serializers
from django.contrib.auth.models import User, Group
from base.serializers import UserSerializer, GroupSerializer, CourseSerializer, AssessmentSerializer, ResultSerializer, StudentSerializer
from base.models import Course, Assessment, Result, Student
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


def grade_result(raw_answers, new_answers):
    # {1: u'0', 2: u'0', 3: u'0', 4: u'0', 5: u'0'}
    # {u'raw': {u'q1': u'3', u'q3': u'2', u'q2': u'3', u'q5': u'4', u'q4': u'0'}, u'graded': [{}, {u'q': u'3', u'a': u'4'}, {}, {}, {}]}
    score = 0
    new_graded = []
    for (q_id, new_correct) in new_answers.items():
        key = "q%s" % q_id
        raw_value = raw_answers[key]
        if new_correct == raw_value:
            score += 1
            new_graded.append({})
        else:
            new_graded.append({'q': q_id, 'a': raw_value})
    return new_graded, score


@csrf_exempt
def my_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #'{"assessment":"a2073014-2bac-444f-bc4d-a7d9c9bde623",
        #"new_answers":[{"question_number":1,"replace":"0"},{"question_number":2,"replace":"0"},{"question_number":3,"replace":"0"},{"question_number":4,"replace":"0"},{"question_number":5,"replace":"0"}]}'
        assessment = Assessment.objects.get(id=data['assessment'])

        new_answers = data['new_answers']
        new_answers2 = {}
        for a in new_answers:
            new_answers2[a['question_number']] = a['replace']
        # Now we fetch and update ALL student answers
        for result in assessment.result_set.all():
            # For each result, we have the "notes" field with
            # {"graded": ["OriginalDataGoesHere"], "raw": {"q2": "3", "q1": "0", "q5": "4", "q4": "0", "q3": "2"}}
            # We need to update graded and the score
            result_obj = json.loads(result.notes)
            (new_graded, score) = grade_result(result_obj['raw'], new_answers2)
            result_obj['graded'] = new_graded
            result.notes = json.dumps(result_obj)
            result.points_earned = score
            result.save()
    return HttpResponse('done')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
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
        serializer.save(professor=[User.objects.get(username=username) for username in self.request.data['professor']])

    def get_queryset(self):
        if not self.request.user.is_anonymous():
            return Course.objects.filter(professor=self.request.user)
        else:
            return Course.objects.none()

class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('course',)
    ordering_fields = ('date',)

    def get_queryset(self):
        if not self.request.user.is_anonymous():
            return Assessment.objects.filter(course__professor=self.request.user)
        else:
            return Assessment.objects.none()

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all().order_by('-submitted')
    serializer_class = ResultSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('student', 'assessment__course')
    ordering_fields = ('assessment__title', 'submitted',)

    def get_queryset(self):
        if not self.request.user.is_anonymous():
            return Result.objects.filter(assessment__course__professor=self.request.user)
        else:
            return Result.objects.none()

    def perform_create(self, serializer):
        assessment = Assessment.objects.get(id=self.request.data['assessment'])
        if assessment.submit_multiple or not assessment.result_set.filter(student=self.request.data['student']).count():
            serializer.save(assessment=assessment)
        else:
            raise serializers.ValidationError("This quiz may not be submitted more than once")


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('email',)

    def get_queryset(self):
        return Student.objects.filter(course__professor=self.request.user).distinct()
