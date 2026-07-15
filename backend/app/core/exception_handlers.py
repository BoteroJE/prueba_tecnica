from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.shared.exceptions import (
    BusinessRuleError,
    ResourceConflictError,
    ResourceNotFoundError,
)


async def resource_not_found_handler(
    request: Request,
    exception: ResourceNotFoundError,
) -> JSONResponse:
    del request

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": exception.detail,
        },
    )


async def resource_conflict_handler(
    request: Request,
    exception: ResourceConflictError,
) -> JSONResponse:
    del request

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": exception.detail,
        },
    )


async def business_rule_handler(
    request: Request,
    exception: BusinessRuleError,
) -> JSONResponse:
    del request

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": exception.detail,
        },
    )


def register_exception_handlers(
    application: FastAPI,
) -> None:
    """
    Registra en FastAPI las excepciones controladas.
    """

    application.add_exception_handler(
        ResourceNotFoundError,
        resource_not_found_handler,
    )

    application.add_exception_handler(
        ResourceConflictError,
        resource_conflict_handler,
    )

    application.add_exception_handler(
        BusinessRuleError,
        business_rule_handler,
    )