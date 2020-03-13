import datetime
from Models import Model, User, Product, ProductUser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Create All Tables
# Model.metadata.create_all(engine)

engine = create_engine('sqlite:///dbORM2.sqlite', echo=True)

Model.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class DataBase:

    def __init__(self):
        pass
        #self.filename = filename
        self.users = None
        self.file = None
        self.load()

    def load(self):
        # self.file = open(self.filename, "r")
        self.file = session.query(User).all()
        self.users = {}

        for line in self.file:
            self.users[line.email] = (line.password, line.type, line.id)
        #self.file.close() para uso de archivos descomentar 12/03/20

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip()] = (password.strip(), name.strip(), DataBase.get_date())
            self.save()
            return 1
        else:
            print("Email exists already")
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            if  self.users[email][0] == password:
                dupla =(self.users[email][1], self.users[email][2])
                return dupla
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + "\n")
    #11/03/20 crud product
    def getProductbyId(self,idProducto):
       return session.query(Product).filter(Product.id == idProducto).first()
    
    def getProducts(self):
       return session.query(Product).all()
    
    #11/03/20 crud product
    def saveProduct(self,newProduct,idProdEdit):
        if idProdEdit=='' or idProdEdit=="0":
            session.add(newProduct)
            session.commit()
        else:#update product
            session.query(Product).filter(Product.id == idProdEdit).update({Product.name: newProduct.name,Product.description:newProduct.description,Product.img:newProduct.img,Product.category:newProduct.category,Product.price:newProduct.price})
            session.commit()
    
    #11/03/20 delete product
    def deleteProduct(self,idDelete):
        session.query(Product).filter(Product.id == idDelete).delete()
        session.commit()
    
    #11/03/20 delete product
    def getProducExist(self,nameProd):
       val= session.query(Product).filter(Product.name == nameProd).first().name
       pass
    
    #12/03/20 trae los articulos del carrito
    def getGiftCat(self, idUsuarioSesion):
        var = session.query(ProductUser).filter(ProductUser.user_id == idUsuarioSesion).all()
        return var

    #12/03/20 trae los articulos del carrito
    def deleteGiftCard(self, idProd):
        session.query(ProductUser).filter(ProductUser.id == idProd).delete()
        session.commit() 
        return True

    #12/03/20  compra realizada
    def emptyCard(self, idProd):
        lstProdUsr =  session.query(ProductUser).filter(ProductUser.user_id == idProd).all()#todos los articulos del carrito del usuario
        for item in lstProdUsr:
            session.query(ProductUser).filter(ProductUser.id == item.id).delete()
        session.commit() 
        return True

    #12/03/20 agregar carrito
    # AgregarCarrito        
    def AgregarCarrito(self,idUsuario, idProd):
        newproductuser = ProductUser(user_id=idUsuario, product_id=idProd)
        session.add(newproductuser)
        session.commit()
        return True
    
    # saveUsr        
    def saveUsr(self,objUsuario):
        session.add(objUsuario)
        session.commit()
        return True

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]


