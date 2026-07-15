from collections.abc import Generator
from datetime import date

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
from app.modules.eps.model import Eps
from app.modules.patients.model import Patient
from app.modules.users.model import User
from app.shared.enums import (
    DocumentType,
    Gender,
    PatientStatus,
    Priority,
    UserRole,
)


@pytest.fixture()
def client() -> Generator[
    TestClient,
    None,
    None,
]:
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
        eps = Eps(
            id=1,
            code="EPS001",
            name="SURA EPS",
            is_active=True,
        )

        user = User(
            id=1,
            username="admin.demo",
            full_name="Administrador Demo",
            password_hash=hash_password(
                "Demo2026*"
            ),
            role=UserRole.ADMIN,
            is_active=True,
        )

        patients = [
            Patient(
                id=1,
                document_type=DocumentType.CC,
                document_number="1000000001",
                full_name="Paciente Uno",
                birth_date=date(1990, 1, 1),
                gender=Gender.FEMALE,
                phone="3000000001",
                eps_id=1,
                priority=Priority.HIGH,
                status=PatientStatus.PENDING,
            ),
            Patient(
                id=2,
                document_type=DocumentType.CC,
                document_number="1000000002",
                full_name="Paciente Dos",
                birth_date=date(1991, 2, 2),
                gender=Gender.MALE,
                phone="3000000002",
                eps_id=1,
                priority=Priority.MEDIUM,
                status=PatientStatus.PENDING,
            ),
            Patient(
                id=3,
                document_type=DocumentType.CC,
                document_number="1000000003",
                full_name="Paciente Tres",
                birth_date=date(1992, 3, 3),
                gender=Gender.FEMALE,
                phone="3000000003",
                eps_id=1,
                priority=Priority.HIGH,
                status=PatientStatus.IN_PROGRESS,
            ),
            Patient(
                id=4,
                document_type=DocumentType.CC,
                document_number="1000000004",
                full_name="Paciente Cuatro",
                birth_date=date(1993, 4, 4),
                gender=Gender.MALE,
                phone="3000000004",
                eps_id=1,
                priority=Priority.LOW,
                status=PatientStatus.ATTENDED,
            ),
            Patient(
                id=5,
                document_type=DocumentType.CC,
                document_number="1000000005",
                full_name="Paciente Cinco",
                birth_date=date(1994, 5, 5),
                gender=Gender.OTHER,
                phone="3000000005",
                eps_id=1,
                priority=Priority.MEDIUM,
                status=PatientStatus.ATTENDED,
            ),
        ]

        session.add(eps)
        session.add(user)
        session.add_all(patients)

        session.commit()

    def override_get_db():
        with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[
        get_db
    ] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

    Base.metadata.drop_all(
        bind=testing_engine
    )

    testing_engine.dispose()


@pytest.fixture()
def auth_headers(
    client: TestClient,
) -> dict[str, str]:
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin.demo",
            "password": "Demo2026*",
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()[
        "access_token"
    ]

    return {
        "Authorization": (
            f"Bearer {access_token}"
        ),
    }


def test_dashboard_requires_authentication(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/v1/dashboard"
    )

    assert response.status_code == 401


def test_dashboard_metrics(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.get(
        "/api/v1/dashboard",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body == {
        "total_patients": 5,
        "pending_patients": 2,
        "in_progress_patients": 1,
        "attended_patients": 2,
        "high_priority_patients": 2,
    }


def test_dashboard_state_totals_match_total(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.get(
        "/api/v1/dashboard",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    state_total = (
        body["pending_patients"]
        + body["in_progress_patients"]
        + body["attended_patients"]
    )

    assert state_total == body["total_patients"]