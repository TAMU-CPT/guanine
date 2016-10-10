from django.contrib import admin
from .models import Course, Assessment, Class, Student, Result

class CourseAdmin(admin.ModelAdmin):
    queryset = Course.objects.all()
    list_display = ('description', 'id', 'name')

class AssessmentAdmin(admin.ModelAdmin):
    queryset = Assessment.objects.all()
    list_display = ('classtime', 'description', 'end_date', 'title', 'id', 'start_date')

class ClassAdmin(admin.ModelAdmin):
    queryset = Class.objects.all()
    list_display = ('description', 'end_date', 'id', 'course', 'start_date')

class StudentAdmin(admin.ModelAdmin):
    queryset = Student.objects.all()
    list_display = ('name', 'email')

class ResultAdmin(admin.ModelAdmin):
    queryset = Result.objects.all()
    list_display = ('points_possible', 'points_earned', 'submitted', 'student', 'assessment', 'id')

admin.site.register(Course, CourseAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Result, ResultAdmin)
