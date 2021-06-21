from peewee import *

from models import *

database = SqliteDatabase('betsy_workshop.db')

def add_tag(product, tag_name):
    tag = Tag.get(Tag.name == tag_name)
    product = Product.get(Product.tags)
    if tag in product:
        None
    else:
        product.tags.add([tag])

def make_records():
    if User.select().where(User.first_name == "Jochum" and User.last_name == "Sloot"):
        None
    else:
        User.create(first_name="Jochum", last_name="Sloot", street="J. de Vriesstraat 1", town="Amsterdam")
    if User.select().where(User.first_name == "David" and User.last_name == "Hello"):
        None
    else:
        User.create(first_name="David", last_name="Hello", street="Maria Anthoinetstraat 1", town="Amsterdam")
    if User.select().where(User.first_name == "Mirjam" and User.last_name == "Sloot"):
        None
    else:
        User.create(first_name="Mirjam", last_name="Sloot", street="Friese tuinen 1", town="Dokkum")
    if User.select().where(User.first_name == "Sabrina" and User.last_name == "Boonstra"):
        None
    else:
        User.create(first_name="Sabrina", last_name="Boonstra", street="Antwerpenstraat 1", town="Rotterdam")
    
    if Tag.select().where(Tag.name == "Domestic"):
        None
    else:
        Tag.create(name="Domestic")
    if Tag.select().where(Tag.name == "Tool"):
        None
    else:
        Tag.create(name="Tool")
    if Tag.select().where(Tag.name == "Garden"):
        None
    else:
        Tag.create(name="Garden")
    if Tag.select().where(Tag.name == "Clothes"):
        None
    else:
        Tag.create(name="Clothes")
    if Tag.select().where(Tag.name == "Games"):
        None
    else:
        Tag.create(name="Games")
        
    if Product.select().where(Product.product_name == "Sweater"):
        None
    else: Product.create(
        product_name="Sweater",
        description="Sweater New-York",
        price_per_unit=50.95,
        tags=[],
        catalog_id=1)
    sweater = Product.get(Product.product_name == "Sweater")
    add_tag(sweater, "Domestic")
    add_tag(sweater, "Clothes")
    if Product.select().where(Product.product_name == "Trouser"):
        None
    else: 
        Product.create(
        product_name="Trouser",
        description="Trouser Levi",
        price_per_unit=40.95,
        tags=[],
        catalog_id=1)
    
    if Product.select().where(Product.product_name == "Cluedo"):
        None
    else: Product.create(
        product_name="Cluedo",
        description="Cluedo the New-York edition",
        price_per_unit=21.95,
        tags=[],
        catalog_id=1)
    
    if UserProduct.select().where(UserProduct.user_id == 1):
        None
    else:
        UserProduct.create(user_id=1, product_id=1, number=2)
        UserProduct.create(user_id=1, product_id=2, number=2)
    if UserProduct.select().where(UserProduct.user_id == 2):
        None
    else:
        UserProduct.create(user_id=2, product_id=1, number=2)
        UserProduct.create(user_id=1, product_id=2, number=3)

    if Product.select().where(Product.product_name == "T-shirt"):
        None
    else:
        Product.create(
            product_name="T-shirt",
            description="T-shirt from Garfield",
            price_per_unit=10.9496,
            number_in_stock=50,
            tags=[], 
            catalog_id=1)

    tshirt_id = Product.get(Product.product_name == "T-shirt")

    if UserProduct.select().where(UserProduct.user_id == 4 and UserProduct.product_id == tshirt_id):
        None
    else:
        UserProduct.create(user_id=4, product_id=tshirt_id, number=10)


