from typing import Optional
from app.ents.base.crud import CRUDBase, db
from app.ents.employee.models import Employee
from app.ents.employee.schema import EmployeeCreate, EmployeeRead


class EmployeeCRUD(CRUDBase[Employee, EmployeeCreate, EmployeeRead, EmployeeRead]):
    def __create_full_name(self, data):
        """Creates the full name of the employee."""
        return data["first_name"] + " " + data["middle_name"] + " " + data["last_name"]

    def read(self, employee_id: int) -> Optional[EmployeeRead]:
        """Read employee with id `employee_id`."""
        return super().read(employee_id)

    def read_multi(self) -> list[EmployeeRead]:
        """Read all employees."""
        return super().read_multi()

    def create(self, data: EmployeeCreate) -> EmployeeRead:
        """Create an employee with `data`."""
        employee = Employee(**data, full_name=self.__create_full_name(data))

        db.session.add(employee)
        db.session.commit()
        db.session.refresh(employee)

        return EmployeeRead(**vars(employee))


crud = EmployeeCRUD(Employee, EmployeeRead)
