from pydantic import BaseModel, ConfigDict


class EpsResponse(BaseModel):
    """
    Información pública de una EPS.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    code: str
    name: str
    is_active: bool