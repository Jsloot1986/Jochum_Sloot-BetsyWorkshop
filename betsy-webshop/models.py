from peewee import Model, SqliteDatabase, IntegerField, DateField, CharField, DecimalField, ManyToManyField, ForeignKeyField, Check


database = SqliteDatabase('betsy_workshop.db', pragmas={"foreign_keys": 1})
# When using sqlite pragma should be put on foreign_keys (only)

class BaseModel(Model):
    class Meta:
        database = database
#if no primary key is defined an implicit primary key is added

class User(BaseModel):
    first_name = CharField()
    last_name = CharField()
    street = CharField()
    town = CharField()

class Tag(BaseModel):
    name = CharField()

class Product(BaseModel):
    product_name = CharField()
    description = CharField()
    price_per_unit = DecimalField(8, 2, True)
    tags = ManyToManyField(Tag)

class UserProduct(BaseModel):
    user_id = ForeignKeyField(User)
    product_id = ForeignKeyField(Product)
    number = IntegerField(constraints=[Check('number >=0')])

class Transaction(BaseModel):
    user_id = ForeignKeyField(User)
    product_id = ForeignKeyField(Product)
    number = IntegerField(constraints=[Check('number>0')])
    sell_date = DateField()
    sell_price = DecimalField(8, 2, True)

ProductTag = Product.tags.get_through_model()

def create_tables():
    with database:
        database.create_tables(
            [User, UserProduct, Product, Transaction, ProductTag, Tag]
        )