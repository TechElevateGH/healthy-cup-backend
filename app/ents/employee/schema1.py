from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    """Base pydantic schema for employees."""

    first_name: str
    middle_name: str = ""
    last_name: str
    email: EmailStr
    active: bool = True


class EmployeeReadEmployee(EmployeeBase):
    ...


class EmployeeReadSupervisor(EmployeeBase):
    ...


class EmployeeClientRead(EmployeeBase):
    ...
