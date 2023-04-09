from flask import Flask
from flask_restful import Api, Resource
import requests
from model import *

app = Flask(__name__)  # initialize Flask
api = Api(app)  # create API

# DishCollection class stores the dishes and perform operations on them
class DishCollection:
    def __init__(self):
        # self.opNum is the number of insertDish operations performed so far.
        # It will be used to generate unique keys to dishes inserted into the collection
        self.opNum = 0
        # self.wrds is a dictionary of the form {key:dish} where key is an integer and dish is a JSON object
        self.dishes = {}  # dishes in the collection

    def insertDish(self, dish_name):
        # This function SHOULD CHECK if the dish already exists and if so return an error
        # Currently, it lets the same dish exist with different keys

        if dish_name in self.dishes:  # dish already exists
            print("DishCollection: dish ", dish_name, " already exists")
            return 0  # key = 0 indicates cannot be inserted
        self.opNum += 1
        key, query = dish_name, dish_name
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url, headers={'X-Api-Key': '6zoIr+IoEg7H2GQGVDxw+g==WdtcKEIt1DOIoGKj'})

        if response.status_code == requests.codes.ok:
            # Convert and insert the JSON response to a the dishes dictionary
            self.dishes[query] = response.json()
            print("DishCollection: inserted dish ", dish_name, " with key ", key)

        else:
            print("Error:", response.status_code, response.text)

        return key

    def findDish(self, key):
        if key in self.dishes:  # the key exists in collection
            dish = self.dishes[key]
            print("DishCollection: found dish ", key)
            return True, dish
        else:
            print("DishCollection: did not find dish", key)
            return False, None  # the key does not exist in the collection

col = DishCollection()  # create DishCollection instance with global scope

# The Dishes class implements the REST operations for the /dishes resource
class Dishes(Resource):
    global col

    # POST adds a dish to /dishes and returns its key.
    def post(self):
        # get argument being passed in query string
        parser = reqparse.RequestParser()  # initialize parse
        # in the query_string, expect "?dish=dish_name" where dish_name is the name of the dish to be added
        parser.add_argument('dish', location='args', required=True)  # location='args' is required, at least on macOS
        args = parser.parse_args()  # parse arguments into a dictionary structure
        dish_name = args["dish"]
        # add dish to collection
        key = col.insertDish(dish_name)
        if key == 0:   # word already exists
            return key, 422
        return key, 201
    def get(self):
        # get argument being passed in query string
        parser = reqparse.RequestParser()  # initialize parse
        # in the query_string, expect "?dish=dish_name" where dish_name is the name of the dish to be added
        parser.add_argument('dish', location='args', required=True)  # location='args' is required, at least on macOS
        args = parser.parse_args()  # parse arguments into a dictionary structure
        dish_name = args["dish"]
        # add dish to collection
        (b, dish) = col.findDish(dish_name)
        if b:
            return dish, 200  # return the dish and HTTP 200 ok code
        else:
            return 0, 404  # return 0 for key and Not Found error code



# MealCollection class stores the meals and perform operations on them
class MealCollection:
    pass


# associate the Resource '/dishes' with the class Dishes
api.add_resource(Dishes, '/dishes')

if __name__ == '__main__':
    # create collection dictionary and keys list
    print("running rest-dish-svr-v1.py")
    # run Flask app.   default part is 5000
    app.run(host='0.0.0.0', port=8000, debug=True)
