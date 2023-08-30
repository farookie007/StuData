from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from results.models import SemesterResult
# Create your views here.


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def refresh(request):
    user = request.user
    user_results = list(user.results.order_by('result_id').all())
    prev_courses = list()

    def is_allowed(course, result_id):
        """Determines the courses that are allowed for cgpa calculation and
        handles complications with 100L Engineering results."""
        return (str(course.ca) != 'nan') and (not(result_id.endswith('100E')) or course.code.startswith('GNS'))
    
    for result in user_results:
        result_id = result.result_id
        prev_courses += [(course.gradient, course.unit) for course in result.courses.all() if is_allowed(course, result_id)]
        try:
            gradients, units = list(zip(*prev_courses))
        except ValueError:
            # if `prev_courses` is empty i.e. none of the course passes validation
            gradients, units = (), ()   # defaults to empty tuple
        result.cgpa = sum(gradients)/ sum(units)
    
    user.cgpa = result.cgpa
    user.save()
    SemesterResult.objects.bulk_update(user_results, fields=('cgpa',))

    return redirect(reverse('dashboard:dashboard'))
