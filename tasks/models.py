from django.db import models


class Task(models.Model):
    STATUS_TODO = "todo"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"
    STATUS_BLOCKED = "blocked"

    STATUS_CHOICES = [
        (STATUS_TODO, "Todo"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_DONE, "Done"),
        (STATUS_BLOCKED, "Blocked"),
    ]

    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True, db_index=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_TODO, db_index=True
    )
    remarks = models.TextField(blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    created_by = models.CharField(max_length=150)
    last_updated_by = models.CharField(max_length=150)

    class Meta:
        ordering = ("-created_on",)

    def __str__(self) -> str:
        return self.title

