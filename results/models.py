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


class Level(models.Model):
    code = models.CharField(max_length=15)


class Semester_Result(models.Model):
    result_id = models.CharField(max_length=30, blank=True, unique=True)
    gpa = models.FloatField(max_length=5, default=0.00)     # stores the gpa of the result
    cgpa = models.FloatField(max_length=5, default=0.00)    # stores the cgpa all previous results

    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='results')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='results')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='results')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='results')


class Course(models.Model):
    Code = models.CharField(max_length=15)
    Title = models.CharField(max_length=150)
    Unit = models.IntegerField()
    Status = models.CharField(max_length=1)     # Todo: Add different choices
    CA = models.FloatField()
    Exam = models.FloatField()
    Total = models.FloatField()
    Grade = models.CharField(max_length=1)      # Todo: Add different choices
    Gradient = models.IntegerField()
    
    course_id = models.CharField(max_length=50, unique=True),
    result = models.ForeignKey(Semester_Result, on_delete=models.CASCADE, related_name='courses')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='courses')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='courses')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f'<Course: {self.code} | {self.title}>'


# class Result(models.Model):
#     semester = models.CharField(max_length=20, blank=True)
#     result_id = models.CharField(max_length=30, blank=True, unique=True)
#     owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='results')
#     level = models.CharField(max_length=5, blank=True)
#     session = models.CharField(max_length=20, blank=True)
#     payload = models.JSONField()
#     gpa = models.FloatField(max_length=5, default=0.00)     # stores the gpa of the result
#     cgpa = models.FloatField(max_length=5, default=0.00)    # stores the cgpa all previous results

#     def __str__(self):
#         return f"<Result: {self.level}L | {self.session} | {self.semester}"
