from typing import Generic, Optional, Type, TypeVar
from pydantic import BaseModel
from flask_sqlalchemy import SQLAlchemy


db: SQLAlchemy = SQLAlchemy()


ModelType = TypeVar("ModelType", bound=db.Model)  # type: ignore
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, ReadSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], read_schema: Type[ReadSchemaType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.model = model
        self.read_schema = read_schema

    def read(self, obj_id: int) -> Optional[ReadSchemaType]:
        """
        Read object with id `obj_id`.
        """
        obj = self.model.query.filter_by(id=obj_id).first()
        return self.read_schema(**vars(obj)) if obj else None

    def read_multi(self, limit: int = 100, skip: int = 0) -> list[ReadSchemaType]:
        """
        Read all objects.
        """
        objs = [self.read_schema(**vars(obj)) for obj in self.model.query.all()]
        return objs

    def create(self, data: CreateSchemaType) -> ReadSchemaType:
        """
        Create a obj with `data`.
        """
        obj = self.model(**data)

        db.session.add(obj)
        db.session.commit()
        db.session.refresh(obj)

        return self.read_schema(**vars(obj))
