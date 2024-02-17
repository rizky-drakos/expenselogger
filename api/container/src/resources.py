from common         import K_PRICE, K_NAME, K_DATE
from flask_restful  import Resource
from flask          import request
        

class HealthStatusAPI(Resource):

    def  __init__(self):
        super().__init__()

    def get(self):
        return { "msg": "Healthy!" }, 200

class ItemsAPI(Resource):

    def __init__(self, db):
        self.db = db
        super().__init__()

    def get(self, username):
        rs = self.db.get_items(username)
        if rs: return rs, 200
        else: return {}, 404

    def post(self, username):
        return self.db.create_item(
            username  = username,
            name    = request.json[K_NAME],
            date    = request.json[K_DATE],
            price   = request.json[K_PRICE]
        ), 201

    def put(self, username):
        return self.db.update_item(
            username  = username,
            name    = request.json[K_NAME],
            date    = request.json[K_DATE],
            price   = request.json[K_PRICE]
        ), 204

    def delete(self, username):
        return self.db.delete_item(
            username  = username,
            name    = request.json[K_NAME],
            date    = request.json[K_DATE],
        ), 204

class ItemsByDate(Resource):

    def __init__(self, db):
        self.db = db
        super().__init__()

    def get(self, username, date):
        rs = self.db.get_items_by_date(username, date)
        if rs: return rs, 200
        else: return {}, 404
