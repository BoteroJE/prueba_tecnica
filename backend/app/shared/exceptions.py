class ApplicationError(Exception):
    """
    Excepción base para errores controlados del sistema.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class ResourceNotFoundError(ApplicationError):
    """
    Se utiliza cuando un recurso solicitado no existe.
    """

    pass


class ResourceConflictError(ApplicationError):
    """
    Se utiliza cuando una operación viola una regla
    de unicidad o produce un conflicto.
    """

    pass


class BusinessRuleError(ApplicationError):
    """
    Se utiliza cuando una operación incumple una
    regla funcional del sistema.
    """

    pass