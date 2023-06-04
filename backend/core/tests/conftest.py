import pytest
from core import models
from rest_framework.test import APIClient

"""
    Fixtures.
"""


@pytest.fixture
def create_user():
    def create(**fields):
        return models.User.objects.create_user(**fields)

    return create


@pytest.fixture
def create_task():
    def create(**fields):
        return models.Task.objects.create(**fields)

    return create


@pytest.fixture
def api_client():
    return APIClient()
