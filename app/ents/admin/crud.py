from typing import Optional

from app.core.security import security
from app.ents.admin.models import Admin
from app.ents.admin.schema import AdminCreateInput, AdminInDB
from app.ents.base.crud import CRUDBase


class AdminCRUD(CRUDBase[Admin, AdminInDB]):
    def read_by_id(self, admin_id: str) -> Optional[Admin]:
        return super().read_by_id(admin_id)

    def read_by_email(self, admin_email: str) -> Optional[Admin]:
        return Admin.query.filter_by(email=admin_email).first()

    def read_multi(self) -> list[Admin]:
        return super().read_multi()

    def create(self, admin_in: AdminCreateInput):
        admin_in.password = security.hash_password(admin_in.password)
        return super().create(AdminInDB.parse_obj(admin_in))


crud = AdminCRUD(Admin)
