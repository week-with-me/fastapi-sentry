from typing import TypeVar, Generic, Type, Optional, List, Dict
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import update, delete, select
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.database import Base, get_db

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        model: Type[ModelType],
        db: Session = Depends(get_db)
    ) -> None:
        self.db = db
        self.model = model
        

    async def get_by_id(self, id: int) -> Optional[Dict]:
        try:
            query    = select(self.model).where(self.model.id == id)
            instance = await self.db.execute(query)
            result   = instance.scala()
            return result
        
        finally:
            self.db.close()
    
    
    async def get_multi(
        self,
        offset: int = 0,
        limit: int = 100
    ) -> Optional[List]:
        try:
            query     = select(self.model).offset(offset).limit(limit)
            instances = await self.db.execute(query)
            result    = instances.scalars().all()
            return result
        
        finally:
            self.db.close()
        
        
    async def create(self, obj_in: CreateSchemaType) -> None:
        try:
            new_data = self.model(**jsonable_encoder(obj_in))
            self.db.add(new_data)
            await self.db.commit()
            
        finally:
            self.db.close()
    
    
    async def update(self, id: int, obj_update: UpdateSchemaType) -> None:
        try:
            query = update(
                self.model
            ).where(
                self.model.id == id
            ).values(**jsonable_encoder(obj_update))
            await self.db.execute(query)
            await self.db.commit()
            
        finally:
            self.db.close()

        
    async def delete(self, id: int) -> None:
        try:
            query = delete(self.model).where(self.model.id == id)
            await self.db.execute(query)
            await self.db.commit()
        
        finally:
            self.db.close()