from django.contrib import admin

from .models import SemesterResult, Course, Semester, Level, Session

# Register your models here.
admin.site.register([SemesterResult, Course, Semester, Level, Session])
