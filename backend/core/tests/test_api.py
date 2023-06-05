import pytest
from core import models
from core.api.serializers import TaskSerializer
from django.shortcuts import reverse
from rest_framework import status


@pytest.mark.django_db
def test_get_tasks_empty_200(api_client):
    url = reverse("tasks")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


@pytest.mark.django_db
def test_get_tasks_200(api_client, create_task):
    create_task(title="Task 1")
    create_task(title="Task 2")

    serializer = TaskSerializer(models.Task.objects.all(), many=True)

    url = reverse("tasks")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == serializer.data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "body",
    [
        {"title": "Title 1", "completed": False},
        {"title": "Title 2", "completed": True},
        {"title": "Title 3"},
    ],
)
def test_post_task_200(api_client, body):
    url = reverse("tasks")
    response = api_client.post(url, data=body)

    task = models.Task.objects.get(pk=response.data.get("id"))

    assert response.status_code == status.HTTP_201_CREATED
    assert task.title == body.get("title")
    assert task.completed == body.get("completed", False)


@pytest.mark.django_db
@pytest.mark.parametrize("body", [{}, {"completed": True}, {"title": "A" * 201}])
def test_post_tasks_400(api_client, body):
    url = reverse("tasks")
    response = api_client.post(url, data=body)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_task_200(api_client, create_task):
    task = create_task(title="Task 1")
    url = reverse("task", kwargs={"pk": task.pk})

    serializer = TaskSerializer(task)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == serializer.data


@pytest.mark.django_db
def test_get_task_404(api_client):
    url = reverse("task", kwargs={"pk": 100})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    "method, body, xstatus",
    [
        ("put", {"title": "Updated", "completed": True}, status.HTTP_200_OK),
        ("put", {"title": "Updated"}, status.HTTP_200_OK),
        ("put", {"completed": True}, status.HTTP_400_BAD_REQUEST),
        ("put", {}, status.HTTP_400_BAD_REQUEST),
        ("patch", {"title": "Updated", "completed": True}, status.HTTP_200_OK),
        ("patch", {"title": "Updated"}, status.HTTP_200_OK),
        ("patch", {"completed": True}, status.HTTP_200_OK),
        ("patch", {}, status.HTTP_200_OK),
    ],
)
def test_put_task(api_client, create_task, method, body, xstatus):
    task = create_task(title="Task 1")
    url = reverse("task", kwargs={"pk": task.pk})

    api_client_method = getattr(api_client, method)
    response = api_client_method(url, data=body)

    assert response.status_code == xstatus

    if xstatus == status.HTTP_200_OK:
        task.refresh_from_db()

        if "title" in body:
            assert task.title == body.get("title")
        if "completed" in body:
            assert task.completed == body.get("completed")


@pytest.mark.django_db
def test_delete_task_204(api_client, create_task):
    task = create_task(title="Task 1")
    url = reverse("task", kwargs={"pk": task.pk})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_task_404(api_client, create_task):
    url = reverse("task", kwargs={"pk": 100})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
