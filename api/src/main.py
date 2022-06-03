import logging

from common         import APP_NAME
from flask          import Flask
from flask_restful  import Api
from resources      import ItemsAPI, ItemsByDate
from db             import LivingExpenseDB

logging.basicConfig(level=logging.INFO)

app     = Flask(APP_NAME)
api     = Api(app)
db      = LivingExpenseDB()

api.add_resource(
    ItemsAPI,
    '/items',
    resource_class_kwargs = { "db": db }
)

api.add_resource(
    ItemsByDate,
    '/items/<string:date>',
    resource_class_kwargs = { "db": db }
)

if __name__ == '__main__':
    app.run()
