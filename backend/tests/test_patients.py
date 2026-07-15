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
def client() -> Generator[TestClient, None, None]:
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

        patient = Patient(
            id=1,
            document_type=DocumentType.CC,
            document_number="1000000001",
            full_name="Ana María Pérez",
            birth_date=date(1990, 5, 20),
            gender=Gender.FEMALE,
            phone="3001234567",
            email="ana@example.com",
            city="Cali",
            eps_id=1,
            priority=Priority.HIGH,
            status=PatientStatus.PENDING,
        )

        session.add_all(
            [
                eps,
                user,
                patient,
            ]
        )

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
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin.demo",
            "password": "Demo2026*",
        },
    )

    token = response.json()[
        "access_token"
    ]

    return {
        "Authorization": f"Bearer {token}",
    }


def test_patients_require_authentication(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/v1/patients"
    )

    assert response.status_code == 401


def test_list_patients(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.get(
        "/api/v1/patients",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["total"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0][
        "document_number"
    ] == "1000000001"


def test_search_patient_by_name(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.get(
        "/api/v1/patients",
        params={
            "search": "Ana María",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_filter_patients(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.get(
        "/api/v1/patients",
        params={
            "status": "Pendiente",
            "priority": "Alta",
            "eps_id": 1,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_create_patient(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/patients",
        headers=auth_headers,
        json={
            "document_type": "CC",
            "document_number": "1234567890",
            "full_name": "Laura Marcela Gómez",
            "birth_date": "1995-08-17",
            "gender": "Femenino",
            "phone": "3005551122",
            "email": "laura@example.com",
            "city": "Cali",
            "eps_id": 1,
            "priority": "Alta",
            "status": "Pendiente",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["document_number"] == (
        "1234567890"
    )
    assert body["eps"]["code"] == "EPS001"


def test_duplicate_document_is_rejected(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/patients",
        headers=auth_headers,
        json={
            "document_type": "CC",
            "document_number": "1000000001",
            "full_name": "Otro paciente",
            "birth_date": "1990-01-01",
            "gender": "Masculino",
            "phone": "3101234567",
            "eps_id": 1,
            "priority": "Media",
            "status": "Pendiente",
        },
    )

    assert response.status_code == 409


def test_future_birth_date_is_rejected(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/patients",
        headers=auth_headers,
        json={
            "document_type": "CC",
            "document_number": "1234500000",
            "full_name": "Paciente futuro",
            "birth_date": "2099-01-01",
            "gender": "Masculino",
            "phone": "3101234567",
            "eps_id": 1,
            "priority": "Media",
            "status": "Pendiente",
        },
    )

    assert response.status_code == 422


def test_update_patient_status(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.patch(
        "/api/v1/patients/1",
        headers=auth_headers,
        json={
            "status": "En atención",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == (
        "En atención"
    )


def test_delete_patient(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    delete_response = client.delete(
        "/api/v1/patients/1",
        headers=auth_headers,
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        "/api/v1/patients/1",
        headers=auth_headers,
    )

    assert get_response.status_code == 404