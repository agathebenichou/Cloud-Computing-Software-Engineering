from .model import Diets, DietsName
from flask import Flask
from flask_restful import Api

# Initialize Flask app
app = Flask(__name__)

# Create API
api = Api(app)

# Associate the Resource /diets with the Diet Class
api.add_resource(Diets, '/diets')

# Associate the Resource /diet/name with the DietsName class
api.add_resource(DietsName, '/diets/<string:name>')


if __name__ == '__main__':

    print("running main.py")

    # run Flask app
    # app.run(host='0.0.0.0',port=5002, debug=True)