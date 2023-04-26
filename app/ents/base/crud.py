from typing import Generic, Optional, Type, TypeVar

from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel

db = SQLAlchemy()

ModelType = TypeVar("ModelType", bound=db.Model)  # type: ignore
DBSchemaType = TypeVar("DBSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, DBSchemaType]):
    """ """

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.model = model

    def read_by_id(self, obj_id: str) -> Optional[ModelType]:
        """
        Read object with id `obj_id`.
        """
        return self.model.query.filter_by(id=obj_id).first()

    def read_multi(self, limit: int = 100, skip: int = 0) -> list[ModelType]:
        """
        Read all objects.
        """
        return self.model.query.all()

    def create(self, data: DBSchemaType) -> Optional[ModelType]:
        """
        Create a obj with `data`.
        """
        ent = self.model(**data.dict())

        db.session.add(ent)
        db.session.commit()
        db.session.refresh(ent)

        return ent

    def update(self, data: DBSchemaType):
        """
        Create a obj with `data`.
        """
        ...

    def delete(self, id: str):
        """
        Delete a obj with  id `id`.
        """
        ...
