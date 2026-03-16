from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.shortcuts import redirect, get_object_or_404

from .forms import TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 50

    def get_queryset(self):
        qs = Task.objects.order_by("-created_on")
        qs = self._apply_filters(qs)
        return qs[:10]

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
        user_id = getattr(self.request.user, "id", None)
        created_by = f"{username} (#{user_id})" if user_id else username
        form.instance.created_by = created_by
        form.instance.last_updated_by = created_by
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")

    def form_valid(self, form):
        username = self.request.user.get_username() or "system"
        user_id = getattr(self.request.user, "id", None)
        form.instance.last_updated_by = f"{username} (#{user_id})" if user_id else username
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task_list")


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"


class TaskStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        status = request.POST.get("status")
        valid_statuses = {key for key, _label in Task.STATUS_CHOICES}
        if status in valid_statuses:
            task.status = status
            username = request.user.get_username() or "system"
            user_id = getattr(request.user, "id", None)
            task.last_updated_by = f"{username} (#{user_id})" if user_id else username
            task.save(update_fields=["status", "last_updated_by", "last_updated_on"])
        return redirect(request.META.get("HTTP_REFERER", "tasks:task_list"))

