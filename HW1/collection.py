from flask import Flask, Api
import requests

app = Flask(__name__)  # initialize Flask
api = Api(app)  # create API

# todo - add documentation to each method


class DishCollection:
    """ DishCollection stores the dishes and performs operations on them
        Each dish is stored in a dictionary with a unique numerical key called id,
        and a value of the following:
            dish name, calories, size (default 100g), sodium, suger
    """

    def __init__(self):
        # self.opNum is the number of insertDish operations performed so far.
        # It will be used to generate unique keys to dishes inserted into the collection
        self.opNum = 0

        # self.dishes is a dictionary of the form {key:dish} where key is an integer and dish is a JSON object
        self.dishes = {}  # dishes in the collection

    def retrieveAllDishes(self):
        """ Retrieve all dicts containing dishes

        :return: dictionary of all dishes in the collection
        """
        print("DishCollection: retrieving all dishes:")
        print(self.dishes)

        # todo - make sure this is indexed by ID
        return self.dishes

    def insertDish(self, dish_name):
        """ Insert a new dish based on dish name
            param: dish_name
            return: id of the new dish (key)
        """
        # This function checks if the dish already exists and if so returns an error

        for id, dish in self.dishes.items():
            if dish[0] == dish_name:
                print("DishCollection: dish ", dish_name, " already exists")
                return 0  # key = 0 indicates cannot be inserted

        self.opNum += 1 # increment latest operation number
        key = self.opNum # assign new key to new operation number

        # Query API Ninja /nutrition
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(dish_name)
        response = requests.get(api_url, headers={'X-Api-Key': '6zoIr+IoEg7H2GQGVDxw+g==WdtcKEIt1DOIoGKj'})

        # Check status code of response
        if response.status_code == requests.codes.ok:
            json_data = response.json()
            self.dishes[key] = [dish_name, json_data['calories'], json_data['serving_size_grams'], json_data['sodium_mg'], json_data['sugar_g']]
            print("DishCollection: dish ", dish_name, " was added")
        else:
            print("Error:", response.status_code, response.text)

        return key

    def findDishID(self, id):
        """ Return a single JSON object of the dish specified by its ID

        :param id: the ID of the dish
        :return: JSON object of the dish
        """

        if id in self.dishes.keys():  # the id exists in collection
            d = self.dishes[id]
            print("DishCollection: found dish ", d, " with id ", id)
            return True, d
        else:
            print("DishCollection: did not find id", id)
            return False, None  # the id does not exist in the collection

    def delDishID(self, id):

        if id in self.dishes.keys():  # the key exists in collection
            d = self.dishes[id]
            del self.dishes[id]
            print("DishCollection: deleted dish ", d, " with id ", id)
            return True, d
        else:
            return False, None  # the key does not exist in the collection

    def delDishName(self, name):

        id_to_delete = None
        for id, dish in self.dishes.items():
            if dish[0] == name:
                id_to_delete = id
                break

        # Delete dish from dictionary by key
        if id_to_delete is not None:
            del self.dishes[id_to_delete]
            print("DishCollection: deleted dish with name ", name)
        else:
            print("DishCollection: did not find dish_name ", name)
            return False, None

    def findDishName(self, name):
        """ Return a single JSON object of the dish specified by its name

        param name: the name of the dish
        return: value of the dish
        """

        fetch_id = None
        for id, dish in self.dishes.items():
            if dish[0] == name:
                fetch_id = id
                break

        # Return dish from dictionary by key
        if fetch_id is not None:
            print("DishCollection: found dish ", self.dishes[fetch_id][0], " with id ", fetch_id)
            return True, self.dishes[fetch_id]
        else:
            print("DishCollection: did not find dish_name ", name)
            return False, None  # the key does not exist in the collection

class MealCollection:
    """ MealCollection stores the dishes and perform operations on them    """

    def __init__(self):
        # self.opNum is the number of insertDish operations performed so far.
        # It will be used to generate unique keys to dishes inserted into the collection
        self.opNum = 0

        # self.dishes is a dictionary of the form {key:dish} where key is an integer and dish is a JSON object
        self.meals = {}  # dishes in the collection

    def retrieveAllMeals(self):
        """ Retrieve all dicts containing meals

        :return: dictionary of all meals in the collection
        """
        print("MealCollection: retrieving all meals:")
        print(self.meals)

        # todo - make sure this is indexed by ID

        return self.meals

    def insertMeal(self, meal_name):
        # This function SHOULD CHECK if the dish already exists and if so return an error
        # Currently, it lets the same dish exist with different keys

        if meal_name in self.meals.values():  # If dish already exists
            print("MealCollection: dish ", meal_name, " already exists")
            return 0  # key = 0 indicates cannot be inserted

        self.opNum += 1  # increment latest operation number
        key = self.opNum  # assign new key to new operation number

        return key

    def delMealID(self, id):

        if id in self.dishes.keys():  # the key exists in collection
            d = self.meals[id]
            del self.meals[id]
            print("MealCollection: deleted meal ", d, " with id ", id)
            return True, d
        else:
            return False, None  # the key does not exist in the collection

    def findMealID(self, id):
        if id in self.meals.keys():  # the key exists in collection
            d = self.meals[id]
            print("MealCollection: found meal ", d, " with id ", id)
            return True, d
        else:
            print("MealCollection: did not find id", id)
            return False, None  # the key does not exist in the collection

    def delMealName(self, name):

        if name in self.meals.values():  # the key exists in collection
            d = self.meals[id] # todo
            del self.meals[id] # todo
            print("MealCollection: deleted meal ", d, " with name ", name)
            return True, d
        else:
            return False, None  # the key does not exist in the collection

    def findMealName(self, name):
        if name in self.meals.values():  # the key exists in collection
            d = self.meals[id] # TODO
            print("MealCollection: found meal ", d, " with name ", name)
            return True, d
        else:
            print("MealCollection: did not find name", name)
            return False, None  # the key does not exist in the collection

    def replaceMeal(self, id, newMeal):
        if id in self.meals.keys():  # the key exists in collection
            self.wrds[id] = newMeal
            print("MealCollection: New meal for id ", id, " is ", newMeal)
            return True, newMeal
        else:  # the key does not exist in the collection
            print("MealCollection: did not find id", id)
            return False, None
