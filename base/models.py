from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import uuid

class Course(models.Model):
    professor = models.ManyToManyField(User)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.name)

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)

    def __str__(self):
        return str(self.name)

class Semester(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    course = models.ForeignKey(Course)
    start_date = models.DateField()
    end_date = models.DateField()
    students = models.ManyToManyField(Student)

    def __str__(self):
        return str(self.name)

class Assessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    semester = models.ForeignKey(Semester)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.title)

class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student)
    assessment = models.ForeignKey(Assessment)
    submitted = models.DateTimeField(blank=True, null=True)
    points_earned = models.FloatField()
    points_possible = models.FloatField()
