import os
import sys
import unittest
import json
import copy

sys.path.insert(0, '..')

from models import Product
from config import db, basedir, connexion_app, app


class TestProducts(unittest.TestCase):
    connexion_app.add_api("swagger.yml")

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')

        self.app = app.test_client()

        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass

    @staticmethod
    def insert_products():
        products = [Product(product_id=1, product_name='Farell',
                            product_price=5.05, size='42'),
                    Product(product_id=2, product_name='Brockman',
                            product_price=58.00, size='45')]
        db.session.add_all(products)
        db.session.commit()

    def test_index(self):
        self.insert_products()
        response = self.app.get('/products', headers={
            'Accept': 'application/json'})

        response_data = json.loads(response.get_data(as_text=True))
        expected_data = [
            {
                'product_id': 1,
                'product_name': 'Farell',
                'product_price': 5.05,
                'size': '42'
            },
            {
                'product_id': 2,
                'product_name': 'Brockman',
                'product_price': 58.00,
                'size': '45'}
        ]

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertEqual(expected_data, response_data)

    def test_get_product(self):
        self.insert_products()
        response = self.app.get('/products/2', headers={
            'Accept': 'application/json'})

        response_data = json.loads(response.get_data(as_text=True))
        expected_data = {
            'product_id': 2,
            'product_name': 'Brockman',
            'product_price': 58.00,
            'size': '45'
        }
        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertEqual(expected_data, response_data)

    def test_get_product_404(self):
        self.insert_products()
        response = self.app.get('/products/6', headers={
            'Accept': 'application/json'})

        response_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(404, response.status_code)
        self.assertEqual('application/problem+json', response.content_type)
        self.assertEqual('Product is not found for id: 6',
                         response_data['detail'])

    def test_create(self):

        # Data that will be sent to /create end-point
        create_data = [
            {
                "product_name": "pr_bulk1",
                "product_price": 10.10,
                "size": "45"
            },
            {
                "product_name": "pr_bulk2",
                "product_price": 20.20,
                "size": "48"
            },
            {
                "product_name": "pr_bulk3",
                "product_price": 30.33,
                "size": "48"
            }
        ]

        # We expect a json with a newly created objects that have their
        # database ids
        expected_data = copy.deepcopy(create_data)
        for x in enumerate(expected_data, 1):
            x[1]['product_id'] = x[0]

        response = self.app.post('/products',
                                 data=json.dumps(create_data),
                                 headers={'Accept': 'application/json',
                                          'Content-Type': 'application/json'})

        response_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(201, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertEqual(expected_data, response_data)

        products = Product.query.all()

        self.assertEqual(3, len(products))

    def test_create_negative(self):

        # Data that will be sent to /create end-point
        create_data = [
            {
                "product_name": "pr_bulk1",
                "product_price": '10.10',
                "size": "45"
            },
            {
                "product_name": "pr_bulk2",
                "product_price": 20.20,
                "size": "48"
            },
            {
                "product_name": "pr_bulk3",
                "product_price": 30.33,
                "size": "48"
            }
        ]

        response = self.app.post('/products',
                                 data=json.dumps(create_data),
                                 headers={'Accept': 'application/json',
                                          'Content-Type': 'application/json'})

        response_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(400, response.status_code)
        self.assertEqual('application/problem+json', response.content_type)
        self.assertEqual("'10.10' is not of type 'number' - '0.product_price'",
                         response_data['detail'])

        products = Product.query.all()

        self.assertEqual(0, len(products))

    def test_create_empty_payload(self):

        # Data that will be sent to /create end-point
        create_data = []

        response = self.app.post('/products',
                                 data=json.dumps(create_data),
                                 headers={'Accept': 'application/json',
                                          'Content-Type': 'application/json'})

        response_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(400, response.status_code)
        self.assertEqual('application/problem+json', response.content_type)
        self.assertEqual(
            "No products for creation are specified", response_data['detail'])

        products = Product.query.all()

        self.assertEqual(0, len(products))

    def test_update(self):
        self.insert_products()

        id_for_update = 2
        name_for_update = 'Christopher'

        update_data = {
            "product_name": name_for_update,
            "product_price": 20.20,
            "size": "48"
        }

        expected_data = copy.deepcopy(update_data)
        expected_data["product_id"] = id_for_update

        response = self.app.put(f'/products/{id_for_update}',
                                data=json.dumps(update_data),
                                headers={'Accept': 'application/json',
                                         'Content-Type': 'application/json'})

        response_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertEqual(expected_data, response_data)

        product = Product.query.filter(
            Product.product_id == id_for_update).one()

        self.assertEqual(name_for_update, product.product_name)

    def test_update_404(self):
        self.insert_products()

        id_for_update = 5
        name_for_update = 'Christopher'

        update_data = {
            "product_name": name_for_update,
            "product_price": 20.20,
            "size": "48"
        }

        response = self.app.put(f'/products/{id_for_update}',
                                data=json.dumps(update_data),
                                headers={'Accept': 'application/json',
                                         'Content-Type': 'application/json'})

        response_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(404, response.status_code)
        self.assertEqual('application/problem+json', response.content_type)
        self.assertEqual(
            f'Product is not found for the id: {id_for_update}',
            response_data['detail'])

    def test_delete(self):
        self.insert_products()

        id_for_delete = 2

        response = self.app.delete(f'/products/{id_for_delete}',
                                   headers={'Accept': 'application/json',
                                            'Content-Type': 'application/json'})

        self.assertEqual(204, response.status_code)
        self.assertEqual('application/json', response.content_type)

        product = Product.query.filter(
            Product.product_id == id_for_delete).one_or_none()

        self.assertEqual(None, product)

    def test_delete_404(self):
        self.insert_products()

        id_for_delete = 5

        response = self.app.delete(f'/products/{id_for_delete}',
                                   headers={'Accept': 'application/json',
                                            'Content-Type': 'application/json'})

        self.assertEqual(404, response.status_code)
        self.assertEqual('application/problem+json', response.content_type)
