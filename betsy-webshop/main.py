__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from datetime import datetime
from models import *
from make_records import *

def search(term):
    return Product.select().where(fn.Upper(Product.product_name).contains(fn.Upper(term)))

def list_user_products(user_id):
    #to collect these three fields it's necessary to combine three tables. The switch is also necessary
    return UserProduct.select(User.first_name, User.last_name, Product.product_name, UserProduct.number).join(Product).switch(UserProduct).join(User).where(UserProduct.user_id == user_id)

def list_products_per_tag(tag_id):
    # In case of a ManytoMany relationship the field of the table underneath are foreignkeyfields.
    return ProductTag.select(Product.product_name, Tag.name).join(Product).switch(ProductTag).join(Tag).where(Tag.id == tag_id)

def update_stock(user_id, product_name, new_quantity):
    # Just a extra check on the table Prouct and user are carried out before adding the product to user_products
    try:
        record = UserProduct.select(Product.product_name, Product.id, UserProduct.user_id).where(
            UserProduct.user_id == user_id).join(Product).where(Product.product_name == product_name).dicts()[0]
        user_product = UserProduct.get(UserProduct.user_id == record['user_id'], UserProduct.product_id == record['id'])
        user_product.number = new_quantity
        user_product.save()
    except:
        print("No record found")

def add_product_to_catalog(user_id, product_name, new_quantity):
    try:
        #if not found the index will be 0. Statement doesn't run completely.
        record = UserProduct.select(Product.product_name, Product.id, UserProduct.user_id).where(UserProduct.user_id == user_id).join(Product).where(Product.product_name == product_name).dicts()[0]
        existing_record = True
    except:
        existing_record = False
    if existing_record == False:
        try:
            product_id_arr = Product.select(Product.id).where(Product.product_name == product_name).dicts()[0]
            UserProduct.create(user_id=user_id, product_id=product_id_arr['id'], number=new_quantity )
        except:
            print("Either the product or the user id doesn't exist yet")

def purchase_product(product_id, buyer_id, quantity, price):
    try:
        user_product = UserProduct.get(UserProduct.user_id == buyer_id and UserProduct.product_id == product_id)
        if user_product.number >= quantity:
            Transaction.create(user_id=buyer_id, product_id=product_id, number=quantity, sell_date=datetime.now(), sell_price=price)
            user_product.number = user_product.number-quantity
            user_product.save()
        else:
            raise ValueError("not enough items in stock")
    except ValueError as e:
        print(e)
    except:
        print(f"No record in user products with values user_id {str(buyer_id)} and product_id {str(product_id)}")

def remove_product(product_name):
    product = Product.get(Product.product_name == product_name)
    product.delete_instance()


create_tables()
"""
purpose create_tables: tables need to be created once
statements underneath: fill database and apply functions
"""

make_records()
chosen_products = search("Sweater")
for product in chosen_products:
    print("product "+product.product_name)

query = list_user_products(1)

for row in query.dicts():
    print("list_user_products "+row.__repr__())

query = list_products_per_tag(1)
print("This are the products with tag id 1")
for tag in query.dicts():
    print(tag)

print("update product in user catalog")

update_stock(1, "Trouser", 25)
purchase_product(67, 1, 1, 70.2345)

remove_product("Cluedo")