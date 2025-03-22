import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

import pytest

pytestmark = pytest.mark.django_db

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "strongpassword123"
    }


@pytest.fixture
def user(user_data):
    return User.objects.create_user(**user_data)


@pytest.fixture
def auth_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }


@pytest.mark.django_db
def test_register_user(api_client):
    payload = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "newpassword123"
    }
    url = reverse("register")  # Пример: путь должен соответствовать urls.py.py
    response = api_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email="newuser@example.com").exists()


@pytest.mark.django_db
def test_login_user(api_client, user_data, user):
    url = reverse("login")  # Пример: путь должен соответствовать urls.py.py
    response = api_client.post(url, {
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_profile_view(api_client, auth_tokens):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_tokens['access']}")
    url = reverse("profile")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "email" in response.data


@pytest.mark.django_db
def test_logout(api_client, auth_tokens):
    url = reverse("logout")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_tokens['access']}")
    response = api_client.post(url, {"refresh": auth_tokens["refresh"]})
    assert response.status_code == status.HTTP_205_RESET_CONTENT


@pytest.mark.django_db
def test_user_update(api_client, auth_tokens):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_tokens['access']}")
    url = reverse("update-profile")
    payload = {
        "first_name": "Updated",
        "last_name": "Name",
        "phone_number": "+70000000000"
    }
    response = api_client.put(url, payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == "Updated"
