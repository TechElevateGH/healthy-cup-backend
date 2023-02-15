from typing import Optional

from app.core.security import security
from app.ents.base.crud import CRUDBase
from app.ents.employee.models import Client
from app.ents.employee.schema import ClientCreateInput, ClientInDB


class ClientCRUD(CRUDBase[Client, ClientInDB]):
    def __create_full_name(self, data: ClientCreateInput):
        """Returns the full name of the client"""
        return data.first_name + " " + data.middle_name + " " + data.last_name

    def read_by_id(self, client_id: str) -> Optional[Client]:
        """Read client with id `client_id`."""
        return super().read_by_id(client_id)

    def read_by_email(self, client_email: str) -> Optional[Client]:
        """Read client with id `client_email`."""
        return Client.query.filter_by(email=client_email).first()

    def read_multi(self) -> list[Client]:
        """Read all employees."""
        return super().read_multi()

    def create(self, client_in: ClientCreateInput) -> Client:
        """Create a client using `client_in`."""
        client_in.password = security.hash_password(client_in.password)

        client_obj = ClientInDB(
            full_name=self.__create_full_name(client_in), **client_in.dict()
        )
        return super().create(client_obj)


crud = ClientCRUD(Client)