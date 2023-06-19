from model import Dishes, DishesID, DishesName, Meals, MealsID, MealsName
from flask import Flask
from flask_restful import Api

""" 
This RESTful API allows users to:
- Create and store dishes
- Create and store old by specifying 3 dishes that comprise that meal (appetizer, main, dessert)
- Retrieve, update, delete dishes and old 

"""

# Initialize Flask app
app = Flask(__name__)

# Create API
api = Api(app)

# Associate the Resource /dishes with the Dishes class
api.add_resource(Dishes, '/dishes')

# Associate the Resource /dishes/ID with the DishesID class
api.add_resource(DishesID, '/dishes/<int:id>')

# Associate the Resource /dishes/ID with the DishesName class
api.add_resource(DishesName, '/dishes/<string:name>')

# Associate the Resource /old with the Meals class
api.add_resource(Meals, '/old')

# Associate the Resource /old/ID with the MealsID class
api.add_resource(MealsID, '/old/<int:id>')

# Associate the Resource /old/ID with the MealsName class
api.add_resource(MealsName, '/old/<string:name>')


if __name__ == '__main__':

    print("running main.py")

    app.run(host='0.0.0.0', port=8000, debug=True)