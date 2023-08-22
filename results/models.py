from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Session(models.Model):
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'<Session: {self.code}>'


class Semester(models.Model):
    code = models.CharField(max_length=1)

    def __str__(self):
        return f'<Semester: {self.code}>'



class Course(models.Model):
    code = models.CharField(max_length=15)
    title = models.CharField(max_length=150)
    unit = models.IntegerField(default=0)
    status = models.CharField(max_length=1)     # Todo: Add different choices
    CA = models.FloatField(max_length=7, null=True)
    exam = models.FloatField(max_length=7, null=True)
    total = models.FloatField(max_length=7, null=True)
    grade = models.CharField(max_length=1)      # Todo: Add different choices
    
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='courses')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='courses')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f'<Course: {self.code} | {self.title}>'













# class Semester(models.Model):
#     code = models.CharField(max_length=20, blank=True)
#     result_id = models.CharField(max_length=30, blank=True, unique=True)
#     level = models.CharField(max_length=5, blank=True)
#     payload = models.JSONField()
#     gpa = models.FloatField(max_length=5, default=0.00)     # stores the gpa of the result
#     cgpa = models.FloatField(max_length=5, default=0.00)    # stores the cgpa all previous results

#     session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='semesters')
#     owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='results')

#     def __str__(self):
#         return f"<Result: {self.level}L | {self.session} | {self.semester}"
