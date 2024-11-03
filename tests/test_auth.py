from http import HTTPStatus

from freezegun import freeze_time
from jwt import decode

from madr.security import create_access_token, settings


def test_get_token(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.username, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token


def test_get_wrong_email_token(client, user):
    response = client.post(
        "/auth/token",
        data={"username": "xxxxxx", "password": user.clean_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "detail" in token


def test_token_inexistent_user(client):
    response = client.post(
        "/auth/token",
        data={"username": "no_user@no_domain.com", "password": "testtest"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}


def test_token_wrong_password(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": "wrong_password"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}


def test_refresh_token(client, user, token):
    response = client.post(
        "/auth/refresh_token",
        headers={"Authorization": f"Bearer {token}"},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


def test_token_expired_dont_refresh(client, user):
    with freeze_time("2023-07-14 12:00:00"):
        response = client.post(
            "/auth/token",
            data={"username": user.username, "password": user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2023-07-14 12:31:00"):
        response = client.post(
            "/auth/refresh_token",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}


def test_jwt():
    data = {"test": "test"}
    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded["test"] == data["test"]
    assert decoded["exp"]
