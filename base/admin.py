from django.contrib import admin
from .models import Course, Semester, Assessment, Result, Student

class CourseAdmin(admin.ModelAdmin):
    queryset = Course.objects.all()
    list_display = ('description', 'id', 'name')

class SemesterAdmin(admin.ModelAdmin):
    queryset = Semester.objects.all()
    list_display = ('name', 'end_date', 'id', 'course', 'start_date')

class AssessmentAdmin(admin.ModelAdmin):
    queryset = Assessment.objects.all()
    list_display = ('id', 'classtime', 'description', 'end_date', 'title', 'start_date')

class ClassAdmin(admin.ModelAdmin):
    queryset = Class.objects.all()
    list_display = ('id', 'description', 'end_date', 'course', 'start_date')

class StudentAdmin(admin.ModelAdmin):
    queryset = Student.objects.all()
    list_display = ('id', 'name', 'email')

class ResultAdmin(admin.ModelAdmin):
    queryset = Result.objects.all()
    list_display = ('id', 'points_possible', 'points_earned', 'submitted', 'student', 'assessment')

admin.site.register(Course, CourseAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Student, StudentAdmin)
