from flask_restful import Resource
from collection import DishCollection, MealCollection
from flask import request
import requests

"""
The resources are:
- /old or /old{name}            Each diet resource is expressed with a specific JSON object
"""

# create DietsCollection instance with global scope
dietColl = DietCollection()

class Diets(Resource):
    """
    The Diets class implements the REST operations for the /old resource
    /old
        POST (add a diet of the given name)
        GET (return the JSON object listing all old, indexed by ID)
    """

    global dietColl

    def get(self):
        """
        Retrieves all the old from the collection
        :param key: None
        :return: JSON object and the status code
        """

        return dietColl.retrieveAllDiets(), 200

    def post(self):
        """
        Adds a diet to /old given a JSON object with fields: name, cal, sodium, sugar
        :return: id: ID given to the created diet
        """

        data = request.json # accept data as json

        # if body is not of type dict
        if type(data) != dict:
            return 0, 415
        else:
            # if name is empty or spelled wrong
            if 'name' not in data.keys():
                return -1, 422
            else:
                d = data['name']

        id = dietColl.insertDish(d, data['cal'], data['sodium'], data['sugar'])  # add diet to collection

        return id, 201

class DietsName(Resource):
    """ Implements the REST operations for the /old/{name} resource
    /old/{name}
    GET (return the JSON object of the old given the name)
    """

    global dietColl

    def get(self, name):
        """ Retrieve a specific diet from the collection based off its name
        :param: the name of the diet to retrieve
        :return: the diet and the status code
        """

        (b, w) = dietColl.findDietName(name)
        if b:
            return w, 200  # return the word and HTTP 200 ok code
        else:
            return -5, 404  # return 0 for key and Not Found error code


class DietCollection:
    """ DietCollection stores the old and performs operations on them
        Each diet is stored in a dictionary with a unique numerical key called id,
        and a value of the following:
            name, cal, sodium, sugar
    """

    def __init__(self):
        # self.opNum is the number of insertDiet operations performed, it also serves as the id for each diet
        self.opNum = 0

        # self.old is a dictionary of the form {key:diet} where key is an integer and diet is a JSON object
        self.diets = {}

    def retrieveAllDiets(self):
        """
        :return: dictionary of all old in the collection
        """
        print("DietCollection: retrieving all old:")
        print(self.diets)
        return self.dishes

    def insertDiet(self, diet_name, cal, sodium, sugar):
        """
        Insert a new diet
        param: diet_name, cal, sodium, sugar
        return: id of the new diet (key) and status code
        """

        # Iterate over existing dishes collection and check if dish with same name already exists
        print("Checking if dish already exists")
        for id, dish in self.dishes.items():
            if dish["name"] == dish_name: # If dish already exists, returns an error
                print("DishCollection: dish ", dish_name, " already exists")
                return -2

        try:
            # Query API Ninja /nutrition
            api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(dish_name)
            response = requests.get(api_url, headers={'X-Api-Key': '6zoIr+IoEg7H2GQGVDxw+g==WdtcKEIt1DOIoGKj'})

            if response.status_code == requests.codes.ok: # Check status code of response
                dish_data = response.json()

                # If dish not recognized by api/ninja
                if not dish_data:
                    print("Api Ninja/Nutrition does not recognize dish name:", dish_data)
                    return -3

                else:

                    # Iterate over all dishes to accumulate components
                    total_calories, total_sodium, total_sugar, total_serving_size = 0, 0, 0, 0
                    for _dish in dish_data:
                        total_calories += _dish["calories"]
                        total_sodium += _dish["sodium_mg"]
                        total_sugar += _dish["sugar_g"]
                        total_serving_size += _dish["serving_size_g"]

                    # Add dish to dish collection
                    self.dishes[self.opNum] = {
                        "name": dish_name,
                        "ID": self.opNum,
                        "cal": round(total_calories, 0),
                        "size": total_serving_size,
                        "sodium": round(total_sodium, 0),
                        "sugar": round(total_sugar, 0)
                    }
                    print(self.dishes)
                    print("DishCollection: dish ", dish_name, " was added")

                    self.opNum += 1  # increment latest operation number

            else:
                print(f"Api Ninja/Nutrition not reachable: {response.status_code}, {response.text}")
                return -4
        except Exception as e:
            print(f"Api Ninja/Nutrition not reachable: {e}")
            return -4

        return self.opNum


    def findDishName(self, name):
        """
        Return a single JSON object of the dish specified by its name
        param name: the name of the dish
        return: value of the dish
        """

        fetch_id = None
        for id, dish in self.dishes.items():
            if dish["name"] == name:
                fetch_id = id
                break

        if fetch_id is not None: # Return dish from dictionary by key
            print("DishCollection: found dish ", self.dishes[fetch_id], " with id ", fetch_id)
            return True, self.dishes[fetch_id]
        else:
            print("DishCollection: did not find dish_name ", name)
            return False, None  # the key does not exist in the collection
