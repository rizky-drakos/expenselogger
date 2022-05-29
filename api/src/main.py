import logging
from pickle import TRUE

from common         import APP_NAME
from flask          import Flask
from flask_restful  import Api
from resources      import ItemsAPI

app     = Flask(APP_NAME)
api     = Api(app)

api.add_resource(ItemsAPI, '/items/<string:date>')

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    app.run(debug=TRUE)