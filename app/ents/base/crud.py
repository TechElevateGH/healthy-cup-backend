from typing import Generic, Optional, Type, TypeVar

from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel

db = SQLAlchemy()


ModelType = TypeVar("ModelType", bound=db.Model)  # type: ignore
DBSchemaType = TypeVar("DBSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, DBSchemaType, ReadSchemaType]):
    """ """

    def __init__(self, model: Type[ModelType], read_schema: Type[ReadSchemaType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.model = model
        self.read_schema = read_schema

    def read_by_id(self, obj_id: str) -> Optional[ReadSchemaType]:
        """
        Read object with id `obj_id`.
        """
        obj = self.model.query.filter_by(id=obj_id).first()
        return self.read_schema(**vars(obj)) if obj else None

    def read_multi(self, limit: int = 100, skip: int = 0) -> list[ReadSchemaType]:
        """
        Read all objects.
        """
        return [self.read_schema(**vars(obj)) for obj in self.model.query.all()]

    def create(self, data: DBSchemaType) -> ReadSchemaType:
        """
        Create a obj with `data`.
        """
        obj = self.model(**data.dict())

        db.session.add(obj)
        db.session.commit()
        db.session.refresh(obj)

        return self.read_schema(**vars(obj))

    def update(self, data: DBSchemaType) -> ReadSchemaType:
        """
        Create a obj with `data`.
        """
        ...

    def delete(self, id: str) -> ReadSchemaType:
        """
        Delete a obj with  id `id`.
        """
        ...
