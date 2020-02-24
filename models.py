from config import db, marshmallow


class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    product_price = db.Column(db.Float)
    product_name = db.Column(db.String(32))
    size = db.Column(db.String(32))


class ProductSchema(marshmallow.ModelSchema):
    class Meta:
        model = Product
        sqlalchemy_session = db.session
