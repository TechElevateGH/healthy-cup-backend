from pydantic import BaseModel, EmailStr


class AdminBase(BaseModel):
    """Base pydantic schema for admins."""

    username: str
    email: EmailStr


class AdminCreateInput(AdminBase):
    """Input schema for creating admins."""

    password: str


class AdminRead(AdminBase):
    """Schema for an admin that is read."""

    id: int


class AdminUpdate(AdminBase):
    """Schema for updating admins."""

    ...


class AdminReadDB(AdminBase):
    """Schema for an admin that is read directly from DB."""

    id: int
    password: str


class AdminInDB(AdminCreateInput):
    """Schema for an admin that is read directly from DB."""

    ...


class AdminLoginInput(BaseModel):
    email: str
    password: str
