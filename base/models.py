from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import uuid

class Course(models.Model):
    professor = models.ManyToManyField(User)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

class Student(models.Model):
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)

class Class(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course)
    start_date = models.DateField()
    end_date = models.DateField()
    students = models.ManyToManyField(Student)

class Assessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    iteration = models.ForeignKey(Class)
    start_date = models.DateField()
    end_date = models.DateField()

class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student)
    assessment = models.ForeignKey(Assessment)
    submitted = models.DateTimeField(blank=True, null=True)
    points_earned = models.FloatField()
    points_possible = models.FloatField()
