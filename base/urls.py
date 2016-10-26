from django.conf.urls import url, include
from rest_framework import routers
from base import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'courses', views.CourseViewSet, 'Course')
router.register(r'assessments', views.AssessmentViewSet, 'Assessment')
router.register(r'results', views.ResultViewSet)
router.register(r'students', views.StudentViewSet)

urlpatterns = [
    url(r'^', include(router.urls, namespace="api")),
]
