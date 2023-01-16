from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    first_name: str
    middle_name: str = ""
    last_name: str
    email: str


class EmployeeIn(EmployeeBase):
    ...


class EmployeeOut(EmployeeBase):
    id: int
