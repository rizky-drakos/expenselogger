import logging

from pickle import TRUE

from common         import APP_NAME
from flask          import Flask
from flask_restful  import Api
from resources      import ItemsAPI, ItemAPI, ItemsByDate
from db             import LivingExpenseDB

logging.basicConfig(level=logging.INFO)

app     = Flask(APP_NAME)
api     = Api(app)
db      = LivingExpenseDB()

api.add_resource(
    ItemsAPI,
    '/<int:userid>/items',
    resource_class_kwargs = { "db": db }
)

api.add_resource(
    ItemAPI,
    '/<int:userid>/items/<string:date>/<string:name>',
    resource_class_kwargs = { "db": db }
)

api.add_resource(
    ItemsByDate,
    '/<int:userid>/items/<string:date>',
    resource_class_kwargs = { "db": db }
)

if __name__ == '__main__':
    app.run()