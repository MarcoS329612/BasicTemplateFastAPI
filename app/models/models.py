from sqlmodel import Field, SQLModel
from typing import Optional
from pydantic import EmailStr

class CustomerBase(SQLModel):
    first_name: str = Field()
    second_name: Optional[str] = Field(default=None)
    last_name: str = Field()
    email: EmailStr = Field()
    password: str = Field()
    phone: Optional[str] = Field(default=None)
    is_active: bool = True
    is_superuser: bool = False

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    __tablename__ = "Customers"
    id: int = Field(default=None, primary_key=True)
