from core.models import Task
from drf_spectacular.utils import extend_schema
from rest_framework import generics

from .serializers import TaskSerializer


class TaskListView(generics.ListCreateAPIView):
    """Get the list of existing tasks."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @extend_schema(description="Create a new task.")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
