from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.core.security import hash_password
from app.db.base import Base
from app.main import app
from app.modules.users.model import User
from app.shared.enums import UserRole


@pytest.fixture(scope="module")
def testing_session_factory():
    testing_engine = create_engine(
        "sqlite://",
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=testing_engine,
        class_=Session,
        autoflush=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(
        bind=testing_engine
    )

    with TestingSessionLocal() as session:
        admin_user = User(
            username="admin.demo",
            full_name="Administrador Demo",
            password_hash=hash_password(
                "Demo2026*"
            ),
            role=UserRole.ADMIN,
            is_active=True,
        )

        inactive_user = User(
            username="inactive.demo",
            full_name="Usuario Inactivo",
            password_hash=hash_password(
                "Demo2026*"
            ),
            role=UserRole.OPERATOR,
            is_active=False,
        )

        session.add_all(
            [
                admin_user,
                inactive_user,
            ]
        )

        session.commit()

    yield TestingSessionLocal

    Base.metadata.drop_all(
        bind=testing_engine
    )

    testing_engine.dispose()


@pytest.fixture(scope="module")
def client(
    testing_session_factory,
) -> Generator[TestClient, None, None]:
    def override_get_db():
        with testing_session_factory() as session:
            yield session

    app.dependency_overrides[
        get_db
    ] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_login_success(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin.demo",
            "password": "Demo2026*",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["expires_in"] == 3600
    assert body["user"]["username"] == (
        "admin.demo"
    )
    assert body["user"]["role"] == "ADMIN"
    assert "password_hash" not in body["user"]


def test_login_wrong_password(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin.demo",
            "password": "incorrect-password",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == (
        "Usuario o contraseña incorrectos."
    )


def test_login_unknown_user(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "unknown.demo",
            "password": "Demo2026*",
        },
    )

    assert response.status_code == 401


def test_inactive_user_cannot_login(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "inactive.demo",
            "password": "Demo2026*",
        },
    )

    assert response.status_code == 401


def test_authenticated_user(
    client: TestClient,
) -> None:
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin.demo",
            "password": "Demo2026*",
        },
    )

    token = login_response.json()[
        "access_token"
    ]

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": (
                f"Bearer {token}"
            ),
        },
    )

    assert response.status_code == 200
    assert response.json()["username"] == (
        "admin.demo"
    )


def test_authenticated_user_requires_token(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/v1/auth/me"
    )

    assert response.status_code == 401


def test_invalid_token_is_rejected(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": (
                "Bearer invalid-token"
            ),
        },
    )

    assert response.status_code == 401