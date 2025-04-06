from fastapi import APIRouter

from models.models import Customer, CustomerCreate, CustomerUpdate
from config.db import SessionDep
from sqlmodel import select, Session, SQLModel
from typing import List
from fastapi import HTTPException, status

customer = APIRouter(prefix="/customers", tags=["customers"])

#Aqui tenemos que creear los basico, CREAR, LEER, LISTAR, ACTUALIZAR Y ELIMINAR 

# Leer

@customer.post("/", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerCreate, session: SessionDep):
    customer_db = Customer.model_validate(customer.model_dump())    
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@customer.get("/{customer_id}", response_model=Customer, status_code=status.HTTP_200_OK)
async def get_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

@customer.get("/", response_model=List[Customer], status_code=status.HTTP_200_OK)
async def get_all_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@customer.patch("/{customer_id}", response_model=Customer, status_code=status.HTTP_200_OK)
async def update_customer(customer_id: int, customer: CustomerUpdate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    customer_data = customer.model_dump(exclude_unset=True)
    customer_data.sqlmodel_update(customer_db)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@customer.delete("/{customer_id}", response_model=Customer, status_code=status.HTTP_200_OK)
async def delete_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    customer.is_active = False
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return {"message": "Customer deleted successfully"}

