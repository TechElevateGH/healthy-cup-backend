from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    """Base pydantic schema for employees."""

    first_name: str
    middle_name: str = ""
    last_name: str
    email: EmailStr


class EmployeeCreateInput(EmployeeBase):
    """Input schema for creating employees."""

    password: str


class EmployeeRead(EmployeeBase):
    """Schema for an employee that is read."""

    id: int
    full_name: str


class EmployeeUpdate(EmployeeBase):
    """Schema for creating employees."""

    ...


class EmployeeCreateDB(EmployeeBase):
    """Database schema for adding an employee."""

    full_name: str = ""
    hashed_password = ""
