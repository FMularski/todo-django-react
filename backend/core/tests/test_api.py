import pytest
from core import models
from core.api.serializers import TaskSerializer
from django.shortcuts import reverse
from rest_framework import status


@pytest.mark.django_db
def test_get_tasks_empty(api_client):
    url = reverse("tasks")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


@pytest.mark.django_db
def test_get_tasks(api_client, create_task):
    create_task(title="Task 1")
    create_task(title="Task 2")

    serializer = TaskSerializer(models.Task.objects.all(), many=True)

    url = reverse("tasks")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == serializer.data
