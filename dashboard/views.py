from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from results.models import SemesterResult
# Create your views here.


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def refresh(request):
    user = request.user
    user_results = list(user.results.order_by('result_id').all())
    prev_courses = list()
    for result in user_results:
        prev_courses += [(course.gradient, course.unit) for course in result.courses.all()]
        gradients, units = list(zip(*prev_courses))
        result.cgpa = sum(gradients)/ sum(units)
    user.cgpa = result.cgpa
    user.save()
    SemesterResult.objects.bulk_update(user_results, fields=('cgpa',))

    return dashboard(request)