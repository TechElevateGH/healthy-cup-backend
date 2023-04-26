from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    """Base pydantic schema for employees."""

    first_name: str
    middle_name: str = ""
    last_name: str
    email: EmailStr
    active: bool = True


class EmployeeCreateInput(EmployeeBase):
    """Input schema for creating employees."""

    password: str


class EmployeeReadEmployee(EmployeeBase):
    id: int
    full_name: str


class EmployeeReadSupervisor(EmployeeBase):
    id: int
    full_name: str


class EmployeeClientReadEmployee(EmployeeBase):
    id: int
    full_name: str


class EmployeeUpdate(EmployeeBase):
    """Schema for updating employees."""

    ...


class EmployeeInDB(EmployeeCreateInput):
    """Database schema for adding an employee."""

    full_name: str = ""


class EmployeeLoginInput(BaseModel):
    email: str
    password: str
