from django.contrib import admin

from .models import Semester_Result, Course, Semester, Level, Session

# Register your models here.
admin.site.register([Semester_Result, Course, Semester, Level, Session])