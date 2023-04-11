from typing import Optional

from app.core.security import security
from app.ents.admin.models import Admin
from app.ents.admin.schema import AdminCreateInput, AdminInDB, AdminReadDB
from app.ents.base.crud import CRUDBase


class AdminCRUD(CRUDBase[Admin, AdminInDB, AdminReadDB]):
    def read_by_id(self, admin_id: str) -> Optional[AdminReadDB]:
        """Read admin with id `admin_id`."""
        return super().read_by_id(admin_id)

    def read_by_email(self, admin_email: str) -> Optional[AdminReadDB]:
        """Read admin with email `admin_email`."""
        admin = Admin.query.filter_by(email=admin_email).first()
        return AdminReadDB(**vars(admin)) if admin else None

    def read_multi(self) -> list[AdminReadDB]:
        """Read all admins."""
        return super().read_multi()

    def create(self, admin_in: AdminCreateInput):
        """Create an admin with `admin_in`."""
        admin_in.password = security.hash_password(admin_in.password)
        return super().create(AdminInDB(**vars(admin_in)))


crud = AdminCRUD(Admin, AdminReadDB)
