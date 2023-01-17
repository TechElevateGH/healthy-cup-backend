from typing import Generic, Optional, Type, TypeVar
from pydantic import BaseModel
from flask_sqlalchemy import SQLAlchemy


db: SQLAlchemy = SQLAlchemy()


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

    def read(self, obj_id: str) -> Optional[ReadSchemaType]:
        """
        Read object with id `obj_id`.
        """
        obj = self.model.query.filter_by(public_id=obj_id).first()
        return self.read_schema(**vars(obj)) if obj else None

    def read_multi(self, limit: int = 100, skip: int = 0) -> list[ReadSchemaType]:
        """
        Read all objects.
        """
        objs = [self.read_schema(**vars(obj)) for obj in self.model.query.all()]
        return objs

    def create(self, data: DBSchemaType) -> ReadSchemaType:
        """
        Create a obj with `data`.
        """
        obj = self.model(**data.dict())

        db.session.add(obj)
        db.session.commit()
        db.session.refresh(obj)

        return self.read_schema(**vars(obj))
