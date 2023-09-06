from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import UpdateView, DetailView

from utils.utils import parse_result_html, get_semester_code
from .forms import ResultUploadForm
from .models import Course, Semester, Session, SemesterResult, Level



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
            return redirect(reverse('dashboard:refresh'))
        form = ResultUploadForm(request.POST, request.FILES)
    # otherwise;
    else:
        form = ResultUploadForm()
    return render(request, 'results/upload.html', {'form': form})


class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'results/course_update.html'
    context_object_name = 'course'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'results/course_detail.html'
    context_object_name = 'course'
