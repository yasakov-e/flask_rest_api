from flask import abort, jsonify
from config import db
from models import Product, ProductSchema


def index():
    """
    This function responds to a request for /products
    with the complete lists of products
    """

    products = Product.query.order_by(Product.product_id).all()
    product_schema = ProductSchema(many=True)

    return product_schema.dump(products)


def get_product(product_id):
    """
    This function responds to a request for /products/{product_id}
    with one matching product
    """
    product = Product.query.filter(
        Product.product_id == product_id).one_or_none()

    if product is not None:
        product_schema = ProductSchema()
        data = product_schema.dump(product)
        return data
    else:
        abort(
            404,
            "Product is not found for id: {product_id}".format(
                product_id=product_id),
        )


def create(products):
    """
    This function responds to a post request for /products
    """
    schema = ProductSchema(many=True)
    new_products = schema.load(products, session=db.session)

    if not new_products:
        abort(400,
              "No products for creation are specified")

    db.session.add_all(new_products)
    db.session.commit()

    return schema.dump(new_products), 201


def update(product_id, product):
    """
    This function updates an esixting product in database
    """

    # Get the products requested from the db into session
    update_product = Product.query.filter(
        Product.product_id == product_id
    ).one_or_none()

    # Did we find an existing product?

    if update_product is not None:

        schema = ProductSchema()
        update = schema.load(product, session=db.session)

        update.product_id = update_product.product_id

        db.session.merge(update)
        db.session.commit()

        return schema.dump(update_product), 200

    else:
        abort(404, f"Product is not found for the id: {product_id}")


def delete(product_id):
    """
    This function deletes a product from the database
    """

    product = Product.query.filter(
        Product.product_id == product_id).one_or_none()

    if product is not None:
        db.session.delete(product)
        db.session.commit()
        return ('', 204)

    else:
        abort(
            404,
            "Product is not found for Id: {product_id}".format(
                product_id=product_id)
        )
