import logging
from common         import K_PRICE, K_USERID, K_NAME, K_DATE
from flask_restful  import Resource
from flask          import request
        

class ItemsAPI(Resource):

    def __init__(self, db):
        self.db = db
        super().__init__()

    def get(self, userid):
        rs = self.db.get_items(int(userid))
        if rs: return rs, 200
        else: return {}, 404

    def post(self, userid):
        return self.db.create_item(
            userid  = userid,
            name    = request.json[K_NAME],
            date    = request.json[K_DATE],
            price   = request.json[K_PRICE]
        ), 201

class ItemsByDate(Resource):

    def __init__(self, db):
        self.db = db
        super().__init__()

    def get(self, userid, date):
        rs = self.db.get_items_by_date(int(userid), date)
        if rs: return rs, 200
        else: return {}, 404

class ItemAPI(Resource):

    def __init__(self, db):
        self.db = db
        super().__init__()

    def put(self, userid, date, name):
        return self.db.update_item(
            userid  = userid,
            name    = name,
            date    = date,
            price   = request.json[K_PRICE]
        ), 204

    def delete(self, userid, date, name):
        return self.db.delete_item(
            userid  = userid,
            name    = date,
            date    = name,
        ), 204
