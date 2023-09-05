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
    """Refreshes the value of the cgpa of the user on the dashboard by calculating the value
    and the gpa value of the individual semester."""
    user = request.user
    user_results = list(user.results.order_by('result_id').all())
    prev_courses = list()

    def is_allowed(course, result_id):
        """Determines the courses that are allowed for cgpa calculation and
        handles complications with 100L Engineering results."""
        return (str(course.ca) != 'nan') and (not(result_id.endswith('100E')) or course.code.startswith('GNS'))
    
    for result in user_results:
        result_id = result.result_id
        curr_courses = [(course.gradient, course.unit) for course in result.courses.all() if is_allowed(course, result_id)]
        prev_courses += curr_courses
    
        try:
            gradients, units = list(zip(*prev_courses))     # getting the gradient and units of the previous courses in a separate list
            c_gradients, c_units = list(zip(*curr_courses)) # getting the gradient and units of the current courses in a separate list
        except ValueError:
            # if `prev_courses` or `curr_courses` is empty i.e. none of the course passes validation
            gradients = units = c_gradients = c_units = ()   # defaults to empty tuple
        result.gpa = sum(c_gradients) / sum(c_units)
        result.cgpa = sum(gradients) / sum(units)
    
    try:
        user.cgpa = result.cgpa
    except UnboundLocalError:   # i.e. `user_results` is empty thereby `result` variable is never defined
        user.cgpa = 0.00    # reset the user result to 0.00
    user.save()
    SemesterResult.objects.bulk_update(user_results, fields=(
        'cgpa',
        'gpa',
    ))

    return redirect(reverse('dashboard:dashboard'))
