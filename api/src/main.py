from flask          import Flask
from flask_restful  import Api
from resources      import Items

app     = Flask("expenselogger")
api     = Api(app)

api.add_resource(Items, '/items')

if __name__ == '__main__':
    app.run()