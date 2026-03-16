from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset()
        return self._apply_filters(qs)

    def _apply_filters(self, qs):
        q = self.request.GET.get("q")
        status = self.request.GET.get("status")
        due_date = self.request.GET.get("due_date")

        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(description__icontains=q)
                | Q(remarks__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        if due_date:
            qs = qs.filter(due_date=due_date)
        return qs


class TaskSearchView(TaskListView):
    """Separate URL for search, reusing the list template and filters."""

    template_name = "tasks/task_list.html"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")

    def form_valid(self, form):
        username = self.request.user.get_username() or "system"
        form.instance.created_by = username
        form.instance.last_updated_by = username
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")

    def form_valid(self, form):
        username = self.request.user.get_username() or "system"
        form.instance.last_updated_by = username
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task_list")

