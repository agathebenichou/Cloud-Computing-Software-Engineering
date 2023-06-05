from meals.model import Dishes, DishesID, DishesName, Meals, MealsID, MealsName
from diets.model import Diets, DietsName
from flask import Flask
from flask_restful import Api

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
api.add_resource(Meals, '/meals')

# Associate the Resource /meal/ID with the MealsID class
api.add_resource(MealsID, '/meal/<int:id>')

# Associate the Resource /meal/name with the MealsName class
api.add_resource(MealsName, '/meal/<string:name>')

if __name__ == '__main__':

    print("running main.py")

    # run Flask app
    app.run(host='0.0.0.0', port=8000, debug=True)