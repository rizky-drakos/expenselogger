from common         import K_PRICE, K_NAME, K_DATE
from flask_restful  import Resource
from flask          import request
from decorators     import jwt_needed
        

class ItemsAPI(Resource):

    def __init__(self, db):
        self.db = db
        super().__init__()

    @jwt_needed
    def get(self, username):
        rs = self.db.get_items(username)
        if rs: return rs, 200
        else: return {}, 404

    @jwt_needed
    def post(self, username):
        return self.db.create_item(
            username  = username,
            name    = request.json[K_NAME],
            date    = request.json[K_DATE],
            price   = request.json[K_PRICE]
        ), 201

class ItemsByDate(Resource):

    def __init__(self, db):
        self.db = db
        super().__init__()

    @jwt_needed
    def get(self, username, date):
        rs = self.db.get_items_by_date(username, date)
        if rs: return rs, 200
        else: return {}, 404

class ItemAPI(Resource):

    def __init__(self, db):
        self.db = db
        super().__init__()

    @jwt_needed
    def put(self, username, date, name):
        return self.db.update_item(
            username  = username,
            name    = name,
            date    = date,
            price   = request.json[K_PRICE]
        ), 204

    @jwt_needed
    def delete(self, username, date, name):
        return self.db.delete_item(
            username  = username,
            name    = name,
            date    = date,
        ), 204
