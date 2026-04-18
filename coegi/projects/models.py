from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import F


def move_task(task_id: int, new_position: int) -> None:
    """
    This Python function `move_task` updates the position of a task within a specified range while
    maintaining the order of tasks based on their positions.

    Args:
      task_id: The `task_id` parameter in the `move_task` function represents the unique identifier of
    the task that you want to move to a new position within a list of tasks. This ID is used to retrieve
    the specific task from the database and update its position accordingly based on the `new_position`
    provided
      new_position: The `move_task` function you provided seems to be handling the repositioning of
    tasks based on a new position provided. It uses database transactions to ensure data consistency.
    """

    with transaction.atomic():
        task = Task.objects.select_for_update().get(pk=task_id)
        old_position = task.position

        if old_position == new_position:
            return

        if old_position > new_position:
            Task.objects.filter(
                status=task.status,
                position__gt=task.position,
                position__lte=new_position,
            ).update(position=F("position") + 1)

        elif old_position < new_position:
            Task.objects.filter(
                status=task.status,
                position__gte=new_position,
                position__lt=task.position,
            ).update(position=F("position") - 1)

        task.position = new_position
        task.save()


class TimeStampedModel(models.Model):
    """An abstract base class that provides self-updating 'created_at' and 'updated_at' fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Project(TimeStampedModel):
    """A class representing a user project, designed to group tasks by purpose."""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=100)
    is_pinned = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name} by {self.owner.username}"


class Task(TimeStampedModel):
    """An item containing an ideia or demand inside a project group, with a status and position."""

    class Status(models.TextChoices):
        BACKLOG = "BACKLOG", "Backlog"
        PENDING = "PENDING", "Pending"
        EXECUTION = "EXECUTION", "Execution"
        COMPLETED = "COMPLETED", "Completed"
        ARCHIVED = "ARCHIVED", "Archived"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True, null=True, max_length=1000)  # noqa: DJ001
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.BACKLOG)
    position = models.PositiveIntegerField(default=0)
    last_status_change = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position"]  # noqa: RUF012
        unique_together = ["status", "position"]  # noqa: RUF012

    def __str__(self) -> str:
        return f"{self.name}, {self.status}"

    def save(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Save function that garantees status change date update on save."""
        if self.pk:
            old_status = Task.objects.get(pk=self.pk).status
            if old_status != self.status:
                self.last_status_change = self.updated_at
        super().save(*args, **kwargs)
