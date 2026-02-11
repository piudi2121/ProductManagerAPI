from fastapi import FastAPI, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy import create_engine, String, Integer, DateTime, Text, Column, func, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

app = FastAPI(title='Product Manager API')

engine = create_engine('sqlite:///products.db', connect_args={'check_same_thread' : False})
LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer(), primary_key=True)
    name = Column(String(127), nullable=False, unique=True)
    description = Column(Text(), nullable=True)
    stock = Column(Integer(), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(127), index=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

Base.metadata.create_all(engine)

class CreateProduct(BaseModel):
    name: str
    description: str
    stock: int 
    price: Decimal
    category: str

class ResponseProduct(BaseModel):
    id: int
    name: str
    description: str
    stock: int 
    price: Decimal
    category: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    price: Optional[Decimal] = None
    category: Optional[str] = None

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()



@app.get('/products/{prod_id}', response_model=ResponseProduct)
def get_product(prod_id:int, db:Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == prod_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found...")
    return product


@app.post('/products', response_model=ResponseProduct)
def create_product(product: CreateProduct, db:Session = Depends(get_db)):
    if db.query(Product).filter(Product.name == product.name):
        raise HTTPException(status_code=400, detail="Product already exists...")
    
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.put('/products/{prod_id}', response_model=ResponseProduct)
def update_product(prod_id:int, product: UpdateProduct, db:Session = Depends(get_db)):
    actual_product = db.query(Product).filter(Product.id == prod_id).first()
    if not actual_product:
        raise HTTPException(status_code=404, detail="Product not found...")
    
    for field, value in product.model_dump(exclude_unset=True).items():
        setattr(actual_product, field, value)
    
    db.commit()
    db.refresh(actual_product)
    return actual_product


@app.delete('/products/{prod_id}')
def delete_product(prod_id:int, db:Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == prod_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found...")
    
    db.delete(product)
    db.commit()
    return {'message' : 'Product deleted successfully'}

@app.get("/products", response_model=list[ResponseProduct])
def show_products(category:Optional[str] = Query(default=None), db:Session = Depends(get_db)):
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    return query.all()