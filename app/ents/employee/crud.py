from typing import Optional

from app.core.security import security
from app.ents.base.crud import CRUDBase
from app.ents.employee.models import Employee
from app.ents.employee.schema import EmployeeCreateInput, EmployeeInDB


class EmployeeCRUD(CRUDBase[Employee, EmployeeInDB]):
    def __create_full_name(self, data: EmployeeCreateInput):
        """Creates the full name of the employee."""
        return data.first_name + " " + data.middle_name + " " + data.last_name

    def read_by_id(self, employee_id: str) -> Optional[Employee]:
        """Read employee with id `employee_id`."""
        return super().read_by_id(employee_id)

    def read_by_email(self, employee_email: str) -> Optional[Employee]:
        """Read employee with email `employee_email`."""
        return Employee.query.filter_by(email=employee_email).first()

    def read_multi(self) -> list[Employee]:
        """Read all employees."""
        return super().read_multi()

    def create(self, employee_in: EmployeeCreateInput) -> Employee:
        """Create an employee with `employee_in`."""
        employee_in.password = security.hash_password(employee_in.password)

        employee_obj = EmployeeInDB(
            full_name=self.__create_full_name(employee_in), **employee_in.dict()
        )
        return super().create(employee_obj)


crud = EmployeeCRUD(Employee)
