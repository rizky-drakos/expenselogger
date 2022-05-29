from common         import K_PRICE, K_USERID, K_NAME, K_DATE
from flask_restful  import Resource
from flask          import request
from db             import LivingExpenseDB

class Items(Resource):

    def __init__(self):
        self.db = LivingExpenseDB()

    def get(self):
        return self.db.get_items_by_userid(1), 200

    def post(self):
        return self.db.create_item(
            userid  = request.json[K_USERID],
            name    = request.json[K_NAME],
            date    = request.json[K_DATE],
            price   = request.json[K_PRICE]
        ), 201

    def put(self):
        return self.db.update_item_by_userid(
            userid  = request.json[K_USERID],
            name    = request.json[K_NAME],
            date    = request.json[K_DATE],
            price   = request.json[K_PRICE]
        ), 204

    def delete(self):
        return self.db.delete_item_by_userid(
            userid  = request.json[K_USERID],
            name    = request.json[K_NAME],
            date    = request.json[K_DATE],
        ), 204