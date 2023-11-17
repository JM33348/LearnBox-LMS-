from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import CourseCreateForm, AssignmentCreateForm, AssignmentSubmissionForm
from .models import Course, Assignment, AssignmentSubmission


class HomeView(ListView):
    paginate_by = 6
    template_name = 'home.html'
    model = Course
    context_object_name = 'course'

    def get_queryset(self):
        return self.model.objects.all()


class CourseCreateView(CreateView):
    template_name = 'core/instructor/course_create.html'
    form_class = CourseCreateForm
    extra_context = {
        'title': 'New Course'
    }
    success_url = reverse_lazy('core:course')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        if self.request.user.is_authenticated and not self.request.user.is_instructor:
            return redirect(reverse_lazy('login'))
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CourseView(ListView):
    model = Course
    template_name = 'core/instructor/courses.html'
    context_object_name = 'course'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')


def course_single(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, "core/instructor/view_course.html", {'course': course})


class AssignmentCreateView(CreateView):
    template_name = 'core/instructor/assignment_create.html'
    form_class = AssignmentCreateForm
    # course_id = form.cleaned_data.get('course_id')  # Adjust this based on your form field name
    extra_context = {
        'title': 'New Course'
    }
    # success_url = reverse_lazy('core:course-view')
    success_url = reverse_lazy('core:course')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        if self.request.user.is_authenticated and not self.request.user.is_instructor:
            return redirect(reverse_lazy('login'))
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AssignmentView(ListView):
    model = Assignment
    template_name = 'core/instructor/assignments.html'
    context_object_name = 'assignment'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        # return self.model.objects.all()
        course_id = self.kwargs.get('course_id')  # Adjust based on your URL structure
    # Filter assignments based on the course
        return self.model.objects.filter(course_id=course_id)


class AssignmentDeleteView(DeleteView):
    model = Assignment
    success_url = reverse_lazy('core:course')


class AssignmentSubmissionView(CreateView):
    template_name = 'core/instructor/assignment_submission.html'
    form_class = AssignmentSubmissionForm
    extra_context = {
        'title': 'New Exam'
    }
    success_url = reverse_lazy('core:course-view')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        if self.request.user.is_authenticated and self.request.user.is_instructor:
            return redirect(reverse_lazy('login'))
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AssignmentSubmissionListView(ListView):
    model = AssignmentSubmission
    template_name = 'core/instructor/assignment_submission_list.html'
    context_object_name = 'assignment_submission'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')


class AssignmentSubmissionDelete(DeleteView):
    model = AssignmentSubmission
    success_url = reverse_lazy('core:assignment-submission-list')
