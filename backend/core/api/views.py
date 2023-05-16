from core.models import Task
from rest_framework import generics

from .serializers import TaskSerializer


class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
