import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from wish.models import Gift

pytestmark = pytest.mark.django_db
User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def gift(user):
    return Gift.objects.create(
        name="Test Gift",
        description="A gift for testing",
        url="https://example.com",
        price=999.99,
        owner=user,
    )


@pytest.mark.django_db
def test_get_all_user_gifts(auth_client, gift):
    response = auth_client.get("/wish/")
    assert response.status_code == 200
    assert response.data[0]["name"] == "Test Gift"


@pytest.mark.django_db
def test_get_single_gift(auth_client, gift):
    response = auth_client.get(f"/wish/{gift.id}/")
    assert response.status_code == 200
    assert response.data["name"] == "Test Gift"


@pytest.mark.django_db
def test_update_gift(auth_client, gift):
    updated_data = {
        "name": "Updated Gift",
        "description": "Updated description",
        "url": "https://updated.com",
        "price": "1234.56",
        "image": "https://updated.com/image.jpg",
        "is_reserved": False,
    }
    response = auth_client.put(f"/wish/{gift.id}/", updated_data, format="json")
    assert response.status_code == 200
    assert response.data["name"] == "Updated Gift"


@pytest.mark.django_db
def test_delete_gift(auth_client, gift):
    response = auth_client.delete(f"/wish/{gift.id}/")
    assert response.status_code == 204
    assert Gift.objects.count() == 0
