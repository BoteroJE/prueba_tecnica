from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.eps.repository import EpsRepository
from app.modules.patients.model import Patient
from app.modules.patients.repository import (
    PatientRepository,
)
from app.modules.patients.schemas import (
    PatientCreate,
    PatientListResponse,
    PatientResponse,
    PatientUpdate,
)
from app.shared.enums import (
    PatientStatus,
    Priority,
)
from app.shared.exceptions import (
    ResourceConflictError,
    ResourceNotFoundError,
)


class PatientService:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

        self.patient_repository = (
            PatientRepository(session)
        )

        self.eps_repository = (
            EpsRepository(session)
        )

    def list_patients(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None,
        patient_status: PatientStatus | None,
        priority: Priority | None,
        eps_id: int | None,
    ) -> PatientListResponse:
        patients, total = (
            self.patient_repository.list(
                page=page,
                page_size=page_size,
                search=search,
                patient_status=patient_status,
                priority=priority,
                eps_id=eps_id,
            )
        )

        total_pages = (
            total + page_size - 1
        ) // page_size

        return PatientListResponse(
            items=[
                PatientResponse.model_validate(
                    patient
                )
                for patient in patients
            ],
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
            has_previous=page > 1,
            has_next=(
                page * page_size < total
            ),
        )

    def get_patient(
        self,
        patient_id: int,
    ) -> PatientResponse:
        patient = (
            self.patient_repository.get_by_id(
                patient_id
            )
        )

        if patient is None:
            raise ResourceNotFoundError(
                "El paciente solicitado no existe."
            )

        return PatientResponse.model_validate(
            patient
        )

    def create_patient(
        self,
        payload: PatientCreate,
    ) -> PatientResponse:
        eps = self.eps_repository.get_by_id(
            payload.eps_id
        )

        if eps is None or not eps.is_active:
            raise ResourceNotFoundError(
                "La EPS seleccionada no existe "
                "o se encuentra inactiva."
            )

        existing_patient = (
            self.patient_repository
            .get_by_document(
                payload.document_number
            )
        )

        if existing_patient is not None:
            raise ResourceConflictError(
                "Ya existe un paciente con "
                "ese número de documento."
            )

        patient = Patient(
            **payload.model_dump()
        )

        try:
            self.patient_repository.add(
                patient
            )

            self.session.commit()

        except IntegrityError as exception:
            self.session.rollback()

            raise ResourceConflictError(
                "No fue posible registrar el paciente "
                "porque existe información duplicada."
            ) from exception

        created_patient = (
            self.patient_repository.get_by_id(
                patient.id
            )
        )

        if created_patient is None:
            raise ResourceNotFoundError(
                "No fue posible recuperar el paciente "
                "después de crearlo."
            )

        return PatientResponse.model_validate(
            created_patient
        )

    def update_patient(
        self,
        patient_id: int,
        payload: PatientUpdate,
    ) -> PatientResponse:
        patient = (
            self.patient_repository.get_by_id(
                patient_id
            )
        )

        if patient is None:
            raise ResourceNotFoundError(
                "El paciente solicitado no existe."
            )

        update_data = payload.model_dump(
            exclude_unset=True
        )

        if "eps_id" in update_data:
            eps = self.eps_repository.get_by_id(
                update_data["eps_id"]
            )

            if eps is None or not eps.is_active:
                raise ResourceNotFoundError(
                    "La EPS seleccionada no existe "
                    "o se encuentra inactiva."
                )

        if "document_number" in update_data:
            existing_patient = (
                self.patient_repository
                .get_by_document(
                    update_data[
                        "document_number"
                    ]
                )
            )

            if (
                existing_patient is not None
                and existing_patient.id
                != patient.id
            ):
                raise ResourceConflictError(
                    "Ya existe otro paciente con "
                    "ese número de documento."
                )

        for field_name, value in (
            update_data.items()
        ):
            setattr(
                patient,
                field_name,
                value,
            )

        try:
            self.session.commit()

        except IntegrityError as exception:
            self.session.rollback()

            raise ResourceConflictError(
                "La actualización genera información "
                "duplicada o inconsistente."
            ) from exception

        updated_patient = (
            self.patient_repository.get_by_id(
                patient.id
            )
        )

        if updated_patient is None:
            raise ResourceNotFoundError(
                "No fue posible recuperar el paciente "
                "después de actualizarlo."
            )

        return PatientResponse.model_validate(
            updated_patient
        )

    def delete_patient(
        self,
        patient_id: int,
    ) -> None:
        patient = (
            self.patient_repository.get_by_id(
                patient_id
            )
        )

        if patient is None:
            raise ResourceNotFoundError(
                "El paciente solicitado no existe."
            )

        try:
            self.patient_repository.delete(
                patient
            )

            self.session.commit()

        except IntegrityError as exception:
            self.session.rollback()

            raise ResourceConflictError(
                "No fue posible eliminar el paciente."
            ) from exception