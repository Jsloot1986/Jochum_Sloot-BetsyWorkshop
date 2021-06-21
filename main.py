__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from datetime import datetime

from make_records import *
from models import *


def search(term):
    return Product.select().where(
        fn.Upper(
            Product.product_name).contains(
            fn.Upper(term)))


def list_user_products(user_id):
    user_products = []
    product_list = Product.select().join(UserProduct).join(User).where(User.id == user_id)

    for product in product_list:
        user_products.append(product.product_name)
    return user_products

#print(list_user_products(1))


def list_products_per_tag(tag_id):
    tag_list = []
    tags = ProductTag.select(ProductTag, Product, Tag).join(Product).switch(ProductTag).join(Tag).where(Tag.id == tag_id)

    for tag in tags:
        tag_list.append((tag.product_name, tag.name))
    return tag_list

#print(list_products_per_tag(1))


def update_stock(user_id, product_name, new_quantity):
    try:
        record = UserProduct.select().join(Product).where(Product.product_name == product_name and UserProduct.user_id == user_id).dicts()[0]
        user_product = UserProduct.get(UserProduct.user_id == record['user_id'], UserProduct.product_id == record['product_id'])
        user_product.number = new_quantity
        user_product.save()
    except:
        print("No record found")


def add_product_to_catalog(user_id, product_name, new_quantity):
    try:
        record = UserProduct.select().join(Product).where(Product.product_name == product_name and UserProduct.user_id == user_id).dicts()[0]
        existing_record = "Y"
        return record
    except:
        existing_record = "N"
    if existing_record == "N":
        try:
            product_id_arr = Product.select(Product.id).where(Product.product_name == product_name).dicts()[0]
            UserProduct.create(user_id=user_id, product_id=product_id_arr['id'], number=new_quantity)
        except:
            print("Either the product or the user_id doesn't exist yet")

    
def purchase_product(product_id, buyer_id, quantity, price):
    try:
        user_product = UserProduct.get(UserProduct.user_id == buyer_id and UserProduct.product_id == product_id)
        if user_product.number >= quantity:
            Transaction.create(user_id=buyer_id, product_id=product_id, number=quantity, sell_date=datetime.now(), sell_price=price)
            user_product.number = user_product.number-quantity
            user_product.save()
        else:
            raise ValueError("not enough goods in stock")
    except ValueError as ve:
        print(ve)
    except:
        print(f"No record in user product with values user_id {str(buyer_id)} and product id {str(product_id)}")


def remove_product(product_name):
    product = Product.get(Product.product_name == product_name)
    product.delete_instance()


make_records()

chosen_product = search("Sweater")
for product in chosen_product:
    print("product "+product.product_name)

query = list_user_products(1)
print(f"the query is: {query}")

product_list = []
for product in query:
    product_list.append(product)
    
print(f"The products in the list are: {product_list}")

query = list_products_per_tag(1)
print("the next one is a list of products with tag id 1")

tag_list = []
for tag in query:
    tag_list.append(tag)

print(f"The tag list is: {tag_list}")

print("update product in user catlog")

update_stock(1, "sweater", 30)
purchase_product(67, 1, 1, 90.1234)

remove_product("T-shirt")
