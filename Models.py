from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Text, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Model = declarative_base()
class User(Model):
    __tablename__ = "users"

    id = Column(Integer,
                primary_key=True)
    type = Column(String(80),
                      unique=False, nullable=False)
    email = Column(String(120),
                   unique=True,
                   nullable=False)
    password = Column(String(80),
                    unique=False, nullable=True)
    # joined = Column(DateTime,
    #                 unique=False,
    #                 nullable=False)
    # join_date=datetime.now()

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Product(Model):
    __tablename__ = "products"

    id = Column(Integer,
                primary_key=True)
    name = Column(String(80),
                    nullable=False)
    description = Column(String(120))
    img = Column(String(80),
                    nullable=False)
    category = Column(String(50),
                    nullable=False)
    price = Column(Float,
                    nullable=False)

    def __repr__(self):
        return '<Product {} /n Description {}>'.format(self.name, self.description)

class ProductUser(Model):
    __tablename__ = "productusers"

    id = Column(Integer,
                primary_key=True)
    user_id = Column(Integer,
                     ForeignKey('users.id'),
                     nullable=False)
    product_id = Column(Integer,
                     ForeignKey('products.id'),
                     nullable=False)
    user = relationship("User", backref="productuser")
    product = relationship("Product", backref="productuser")

    def __repr__(self):
        return '<ProductUser userID: {} productID: {} >'.format(self.user_id, self.product_id)