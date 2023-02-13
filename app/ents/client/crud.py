from typing import Optional

from app.core.security import security
from app.ents.base.crud import CRUDBase
from app.ents.employee.models import Client
from app.ents.employee.schema import ClientCreateInput, ClientInDB


class ClientCRUD(CRUDBase[Client, ClientInDB]):
    def __create_full_name(self, data: ClientCreateInput):
        pass

    def read_by_id(self, client_id: str) -> Optional[Client]:
        return super().read_by_id(client_id)


crud = ClientCRUD(Client)