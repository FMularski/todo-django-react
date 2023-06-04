import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

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
