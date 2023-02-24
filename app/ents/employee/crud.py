from typing import Optional

from app.core.security import security
from app.ents.base.crud import CRUDBase
from app.ents.employee.models import Employee
from app.ents.employee.schema import (EmployeeCreateInput, EmployeeInDB,
                                      EmployeeRead)


class EmployeeCRUD(CRUDBase[Employee, EmployeeInDB, EmployeeRead]):
    def __create_full_name(self, data: EmployeeCreateInput):
        """Creates the full name of the employee."""
        return data.first_name + " " + data.middle_name + " " + data.last_name

    def read_by_id(self, employee_id: str) -> Optional[EmployeeRead]:
        """Read employee with id `employee_id`."""
        return super().read_by_id(employee_id)

    def read_by_email(self, employee_email: str) -> Optional[EmployeeInDB]:
        """Read employee with email `employee_email`."""
        employee = Employee.query.filter_by(email=employee_email).first()
        return EmployeeInDB(**vars(employee))

    def read_multi(self) -> list[EmployeeRead]:
        """Read all employees."""
        return super().read_multi()

    def create(self, data: EmployeeCreateInput) -> EmployeeRead:
        """Create an employee with `data`."""
        employee_obj = EmployeeInDB(
                full_name=self.__create_full_name(data),
                hashed_password=security.hash_password(data.password),
            **data.dict(
                exclude={"password"},
            )
        )
        return super().create(employee_obj)


crud = EmployeeCRUD(Employee, EmployeeRead)
