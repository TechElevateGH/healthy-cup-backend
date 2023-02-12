from typing import Optional

from app.core.security import security
from app.ents.base.crud import CRUDBase
from app.ents.employee.models import Client
from app.ents.employee.schema import ClientCreateInput, ClientInDB


class ClientCRUD(CRUDBase[Client, ClientInDB]):
    pass
crud = ClientCRUD(Client)