from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "due_date", "created_by", "created_on")
    list_filter = ("status", "due_date", "created_on")
    search_fields = ("title", "description", "remarks", "created_by")

