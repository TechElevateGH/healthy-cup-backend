from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    """Base pydantic schema for employees."""

    first_name: str
    middle_name: str = ""
    last_name: str
    full_name: str = ""
    email: EmailStr

    def __setitem__(self, field, value):
        self.field = value


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
