from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    """Base pydantic schema for clients."""

    first_name: str
    middle_name: str = ""
    last_name: str
    email: EmailStr
    active: bool = True


class ClientCreateInput(ClientBase):
    """Input schema for creating clients."""

    password: str


class ClientReadClient(ClientBase):
    id: int
    full_name: str


class ClientUpdate(ClientBase):
    """Schema for updating employees."""

    ...


class ClientInDB(ClientCreateInput):
    """Database schema for adding an employee."""

    full_name: str = ""


class ClientLoginInput(BaseModel):
    email: str
    password: str

