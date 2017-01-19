from django.contrib import admin
from .models import Course, Assessment, Result, Student

class CourseAdmin(admin.ModelAdmin):
    queryset = Course.objects.all()
    list_display = ('name', 'id', 'description')

class AssessmentAdmin(admin.ModelAdmin):
    queryset = Assessment.objects.all()
    list_display = ('id', 'description', 'date', 'course', 'title', 'start_date', 'end_date')

class StudentAdmin(admin.ModelAdmin):
    queryset = Student.objects.all()
    list_display = ('id', 'name', 'email')

class ResultAdmin(admin.ModelAdmin):
    queryset = Result.objects.all()
    list_display = ('id', 'points_possible', 'points_earned', 'submitted', 'student', 'assessment', 'notes')

admin.site.register(Course, CourseAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Student, StudentAdmin)
