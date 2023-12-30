from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import ResultUploadForm
from .models import Course, Semester, Session, SemesterResult, Level
from utils.utils import parse_result_html, get_semester_code




@login_required
def upload_result_view(request):
    # if a POST request is sent
    if request.method == 'POST':
        form = ResultUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_results = form.cleaned_data["file"]
            user = request.user
            COURSES_LIST = list()
            SEMESTERRESULT_LIST = list()

            for file in uploaded_results:
                dfs, session_code, level_code, fac, dept = parse_result_html(file.file)
                # update the user bio-data
                user.faculty, user.department = fac, dept
                # create a new `Session` if it doesn't exist 
                session = Session.objects.get_or_create(code=session_code)[0]
                level = Level.objects.get_or_create(code=level_code)[0]

                # looping over each semester result in the file
                for df in dfs:
                    # create a new `Semester` if it doesn't exist already
                    df.columns = df.columns.str.lower()
                    semester_code = get_semester_code(df)
                    result_id = f'{user.matric}:{session_code}/{semester_code}/{level_code}{"E" if fac == "Engineering and Technology" else ""}'    # unique id to differentiate each result
                    semester = Semester.objects.get_or_create(code=semester_code)[0]
                    result = SemesterResult.objects.get_or_create(
                        result_id=result_id,
                        level=level,
                        semester=semester,
                        session=session,
                        owner=user,
                    )[0]
                    SEMESTERRESULT_LIST.append(result)

                    for course_code in df.index:
                        location = df.loc[course_code]
                        course_id = f"{user.matric}:{session_code}|{course_code}"
                        kwargs = location.to_dict()
                        kwargs.update(
                            {
                                'code': location.name,
                                'course_id': course_id,
                                'result': result,
                                'session': session,
                                'owner': user,
                                'semester': semester,
                            }
                        )
                        course = Course(**kwargs)
                        COURSES_LIST.append(course)
            # Bulk creating the list of courses uploaded
            Course.objects.bulk_create(
                COURSES_LIST,
                batch_size=500,
                update_conflicts=True,
                update_fields=('status', 'ca', 'exam', 'total', 'grade', 'gradient'),
                unique_fields=('course_id',),
            )
            # Bulk updating the list of each semester's gpa
            SemesterResult.objects.bulk_update(
                SEMESTERRESULT_LIST,
                batch_size=500,
                fields=('gpa',),
            )
            # saving the user
            user.save()
            messages.success(request, "Upload successful")
            return redirect(reverse('dashboard:dashboard'))
        form = ResultUploadForm(request.POST, request.FILES)
    # otherwise;
    else:
        form = ResultUploadForm()
    return render(request, 'results/upload.html', {'form': form})


class CourseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Course
    template_name = 'results/course_detail.html'
    context_object_name = 'course'

    def test_func(self):
        """Allows only the owner of the course to perform operation"""
        return (self.request.user == self.get_object().owner)


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    template_name = 'results/course_update.html'
    context_object_name = 'course'
    success_url = reverse_lazy('dashboard:dashboard')
    fields = (
        'ca',
        'exam',
    )

    def test_func(self):
        """Allows only the owner of the course to perform operation
        ...and also only if the course scores are null values."""
        obj = self.get_object()
        return (self.request.user == obj.owner) # and ('nan' in [str(x) for x in [obj.ca, obj.exam, obj.total, obj.grade]])
    
    @staticmethod
    def get_grade(score, E_allowed=True):
        """
        Gets the corresponding grade of a particular `score`.
        
        params:
            E_allowed :bool: represents whether grade 'E' is allowed for
            the user. E.g. people admitted in session 2017/18 do not have
            'E' grade.
        returns:
            grade: character representing the grade.
        """
        if score >= 70:
            return 'A'
        elif score >= 60:
            return 'B'
        elif score >= 50:
            return 'C'
        elif score >= 45:
            return 'D'
        elif score >= 40 and E_allowed:
            return 'E'
        else:
            return 'F'

    def form_valid(self, form):
        course = form.save(commit=False)
        course.total = course.ca + course.exam
        course.grade = self.get_grade(course.total, E_allowed=not(course.owner.matric.startswith('17/')))
        gradient = {
            'A': 5,
            'B': 4,
            'C': 3,
            'D': 2,
            'E': 1,
            'F': 0,
        }.get(course.grade, None)

        if gradient is None:
            messages.error(self.request, "Invalid grade character")
            return self.form_invalid(form)
        course.gradient = gradient * course.unit
        return super().form_valid(form)


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'results/course_delete.html'
    success_url = reverse_lazy('dashboard:dashboard')

    def test_func(self):
        """Allows only the owner of the course to perform operation"""
        return self.request.user == self.get_object().owner
