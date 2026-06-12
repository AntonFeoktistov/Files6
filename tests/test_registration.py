import pytest
from django.contrib.auth import get_user_model

from tests.urls import urls

User = get_user_model()
pytestmark = pytest.mark.django_db


def test_register_success(client):

    response = client.post(
        urls.register_url,
        {
            "username": "newuser",
            "password1": "pass123",
            "password2": "pass123",
        },
    )

    assert response.status_code == 302
    assert User.objects.filter(username="newuser").exists()


def test_password_no_two_latin_letters(client):

    response = client.post(
        urls.register_url,
        {
            "username": "testuser",
            "password1": "123456",
            "password2": "123456",
        },
    )

    form = response.context["form"]
    error_text = form.errors["password1"][0]

    assert "минимум 2 буквы" in error_text.lower()
    assert not User.objects.filter(username="testuser").exists()


def test_password_no_two_digits(client):

    response = client.post(
        urls.register_url,
        {
            "username": "testuser",
            "password1": "abchello",
            "password2": "abchello",
        },
    )

    form = response.context["form"]
    error_text = form.errors["password1"][0]

    assert "2 цифры" in error_text.lower()
    assert not User.objects.filter(username="testuser").exists()


def test_passwords_do_not_match(client):

    response = client.post(
        urls.register_url,
        {
            "username": "testuser",
            "password1": "Valid123",
            "password2": "Different456",
        },
    )

    form = response.context["form"]
    error_text = form.errors["password2"][0]

    assert "пароли не совпадают" in error_text.lower()
    assert not User.objects.filter(username="testuser").exists()


def test_register_duplicate_username(client, test_user):

    response = client.post(
        urls.register_url,
        {
            "username": "testuser",
            "password1": "pass123",
            "password2": "pass123",
        },
    )

    error_text = response.context["form"].errors["username"][0]
    assert "already exists" in error_text.lower() or "существует" in error_text.lower()


def test_username_too_long(client):

    response = client.post(
        urls.register_url,
        {
            "username": "a" * 26,
            "password1": "ab12cd",
            "password2": "ab12cd",
        },
    )

    form = response.context["form"]
    error_text = form.errors["username"][0]

    assert "25" in error_text
    assert not User.objects.filter(username="a" * 26).exists()


def test_password_too_long(client):
    long_password = "p" * 26 + "ab12"

    response = client.post(
        urls.register_url,
        {
            "username": "testuser",
            "password1": long_password,
            "password2": long_password,
        },
    )

    form = response.context["form"]
    error_text = form.errors["password1"][0]

    assert "25" in error_text
    assert not User.objects.filter(username="testuser").exists()
