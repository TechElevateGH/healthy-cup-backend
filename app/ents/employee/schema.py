from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    """Base pydantic schema for employees."""

    first_name: str
    middle_name: str = ""
    last_name: str
    email: EmailStr


class EmployeeCreate(EmployeeBase):
    """Schema for creating employees."""

    ...


class EmployeeRead(EmployeeBase):
    """Schema for read employees"""

    id: int
    full_name: str

class EmployeeUpdate(EmployeeBase):
    """Schema for creating employees."""

    ...