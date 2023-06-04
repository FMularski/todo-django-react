import json

import pytest
from core import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.management import call_command
from django.db.utils import IntegrityError

User = get_user_model()

"""
    Fixtures
"""


@pytest.fixture
def create_user():
    def create(**fields):
        return User.objects.create_user(**fields)

    return create


@pytest.fixture
def create_task():
    def create(**fields):
        return models.Task.objects.create(**fields)

    return create


"""
    User model tests.
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, password",
    [
        ("test", "testpass"),
        ("user", "123test123"),
    ],
)
def test_create_user(create_user, username, password):
    user = create_user(username=username, password=password)

    assert user.username == username
    assert check_password(password, user.password)


@pytest.mark.django_db
def test_create_user_no_username(create_user):
    with pytest.raises(TypeError) as e:
        create_user()


@pytest.mark.django_db
def test_users_command_fixture():
    with open(settings.BASE_DIR / "core/fixtures/users.json") as fixture_file:
        data = json.loads(fixture_file.read())
        users_count = len(data)

    assert User.objects.count() == 0
    call_command("loaddata", "users.json")
    assert User.objects.count() == users_count


"""
    Task model tests.
"""


@pytest.mark.django_db
@pytest.mark.parametrize(
    "title, completed",
    [
        ("Test task", True),
        ("Test task 2", False),
    ],
)
def test_create_task(create_task, title, completed):
    task = create_task(title=title, completed=completed)
    assert task.title == title
    assert task.completed == completed


@pytest.mark.django_db
def test_create_task_default_not_completed(create_task):
    task = create_task(title="Test task")
    assert task.completed == False


@pytest.mark.django_db
def test_create_task_title_required(create_task):
    with pytest.raises(IntegrityError) as e:
        create_task(title=None)


@pytest.mark.django_db
def test_tasks_command_fixture():
    with open(settings.BASE_DIR / "core/fixtures/tasks.json") as fixture_file:
        data = json.loads(fixture_file.read())
        tasks_count = len(data)

    assert models.Task.objects.count() == 0
    call_command("loaddata", "tasks.json")
    assert models.Task.objects.count() == tasks_count
