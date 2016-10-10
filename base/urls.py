from django.conf.urls import url, include
from rest_framework import routers
from base import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'assessments', views.AssessmentViewSet)
router.register(r'classes', views.ClassViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'results', views.ResultViewSet)

urlpatterns = [
    url(r'^base/', include(router.urls)),
]