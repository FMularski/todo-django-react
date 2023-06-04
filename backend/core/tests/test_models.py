import json

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.management import call_command

User = get_user_model()


@pytest.fixture
def create_user():
    def create(**fields):
        return User.objects.create_user(**fields)

    return create


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
