from django.urls import path

from .views import TaskDetailView, TaskListView

urlpatterns = [
    path("tasks/", TaskListView.as_view(), name="tasks"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task"),
]
