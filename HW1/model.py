from flask_restful import Resource, reqparse
from collection import DishCollection, MealCollection
from flask import Flask, request
"""
The resources are:

- /meals                            This is a collection class, containing all the meals
- /meals/{ID} or /meals/{name}      Each meal resource is expressed with a specific JSON object
- /dishes                           This is a collection class, containing all the dishes 
- /dishes/{ID} or /dishes/{name}    Each dish resource is expressed with a specific JSON object
"""

# todo  - check all functionality against requirements in powerpoint

# create DishCollection instance with global scope
dishColl = DishCollection()

# todo- seeing weird behavior with dish collection being deleted


class Dishes(Resource):
    """
    The Dishes class implements the REST operations for the /dishes resource
    /dishes
        POST (add a dish of the given name)
        GET (return the JSON object listing all dishes, indexed by ID)
    """

    global dishColl

    # COMPLETED
    def get(self):
        """
        Retrieves a specific dish from the collection
        :param key: the key used to search for a dish (either ID or name)
        :return: JSON object listing all dishes (indexed by ID) and the status code
        """

        return dishColl.retrieveAllDishes(), 200

    def post(self):
        """
        Adds a dish to /dishes and returns its ID
        :param key: name used to add a dish
        :return: id: dish ID given to the dish
        """

        # get argument being passed in query string
        parser = reqparse.RequestParser()  # initialize parse

        # in the query_string, expect "?name=d" where d is the name of the dish to be added
        parser.add_argument('name', location='args', required=True, help=f"Query String expects 'name'")
        args = parser.parse_args()  # parse arguments into a dictionary structure

        d = args["name"] #parse dish name from arguments
        id = dishColl.insertDish(d)  # add d to collection

        # todo = apply these cors
        ''' 
        • 0 means that request content-type is not application/json. Status code 415 (Unsupported Media Type)
        • -1 means that 'name' parameter was not specified in the message body. Status code 422 (Unprocessable Content)
        '''
        if id is None:   # dish already exists
            return id, 422
        elif id == -4: # api.api-ninjas.com/v1/nutrition was not reachable
            return 504
        return id, 201

    # COMPLETED
    def delete(self):
        """ Deleting the entire collection is not allowed

        :return: return error message
        """

        return "This method is not allowed for request URL", 405


class DishesID(Resource):
    """ Implements the REST operations for the /dishes/{ID} resource

    /dishes/{ID}
        GET (return the JSON object of the dish given the ID)
        DELETE (delete a dish of the given ID)
    """

    global dishColl

    # COMPLETED
    def get(self, id):
        """ Retrieve a specific dish from the collection based off its ID

        :param id: the ID of the dish to retrieve
        :return: the dish JSON object and the status code
        """

        (status, dish_obj) = dishColl.findDishID(id)
        if status:
            return dish_obj, 200  # return the word and HTTP 200 ok code
        else:
            return -5, 404  # return 0 for key and Not Found error code

    # COMPLETED
    def delete(self, id):
        """ Delete a dish from the collection based off its ID

        :param id: the ID of the dish to delete
        :return: the deleted dish ID and the status code
        """

        (status, dish_id) = dishColl.delDishID(id)
        if status:
            return dish_id, 200  # return deleted dosj and HTTP 200 ok code
        else:
            return -5, 404  # return 0 for id value (error) and Not Found error code


class DishesName(Resource):
    """ Implements the REST operations for the /dishes/{name} resource

    /dishes/{name}
        GET (return the JSON object of the dish given the name)
        DELETE (delete a dish of the given name)
    """

    global dishColl

    # COMPLETED
    def delete(self, name):
        """ Delete a dish from the collection based off its name

        :param name: the ma,e of the dish to delete
        :return: the deleted dish and the status code
        """

        (status, dish_id) = dishColl.delDishName(name)
        if status:
            return dish_id, 200  # return deleted word and HTTP 200 ok code
        else:
            return -5, 404  # return 0 for key value (error) and Not Found error code

    # COMPLETED
    def get(self, name):
        """ Retrieve a specific dish from the collection based off its ID

        :param id: the ID of the dish to retrieve
        :return: the dish and the status code
        """

        (status, dish_obj) = dishColl.findDishName(name)
        if status:
            return dish_obj, 200  # return the word and HTTP 200 ok code
        else:
            return -5, 404  # return 0 for key and Not Found error code
                            # Why -5, isnt it supposed to be 0?


# create MealCollection instance with global scope
mealColl = MealCollection()


class Meals(Resource):
    """ The Meal class implements the REST operations for the /meals resource

    /meals
        POST (add a meal of the given name)
        GET (return the JSON object listing all meals, indexed by ID)
    """

    global dishColl
    global mealColl

    def get(self):
        """ Retrieves a specific meal from the collection

        :return: all meal objects and status code
        """

        return mealColl.retrieveAllMeals(), 200

    def post(self):
        """
        Adds a meal to /meals
        :param name: name used to add a meal, appetizer: appetizer dish ID, main: main dish ID, dessert: dessert dish ID
        :return: id: ID given to the meal
        """

        '''
        post will be a JSON object with fields: name, appetizer, main, dessert
        Will parse JSON object and pass components using dishCollection
        Passes Dish IDs, not names
        '''
        data = request.json
        meal_name = data['name']
        appetizer_id = data['appetizer']
        main_id = data['main']
        dessert_id = data['dessert']

        '''
        ##### todo:
        • 0 means that request content-type is not application/json. Status code 415 (Unsupported Media Type)
        • -1 means that one of the required parameters was not given or not specified correctly. Status code 422
        (Unprocessable Entity)
        • -2 means that a meal of the given name already exists. Status code 422 (Unprocessable Entity)
        • -6 means that one of the sent dish IDs (appetizer, main, dessert) does not exist. Status code 422
        (Unprocessable Entity)*
        '''

        # add d to collection
        key = mealColl.insertMeal(meal_name, appetizer_id, main_id, dessert_id, dishColl)
        if key == 0:  # meal already exists
            return -2, 422
        return key, 201


class MealsID(Resource):
    """ Implements the REST operations for the /meals/{ID} resource

    /meals/{ID}
        GET (return the JSON object of the meal given the ID)
        DELETE (delete a meal of the given ID)
        PUT (add a meal of the given ID)
    """

    global mealColl

    def delete(self, id):
        """ Delete a meal from the collection based off its ID

        :param id: the ID of the meal to delete
        :return: the deleted meal and the status code
        """

        # todo
        '''
        retur id of the meal deleted 
        if meal id not does not exist, return -5, 404 
        '''

        b, w = mealColl.delMealID(id)
        if b:
            return w, 200  # return deleted meal and HTTP 200 ok code
        else:
            return 0, 404  # return 0 for key value (error) and Not Found error code

    def get(self, id):
        """
        Retrieve a specific meal from the collection based off its ID
        :param id: the ID of the meal to retrieve
        :return: the meal and the status code
        """

        # todo
        ''' send id of the meal and receive back the json meal object
        if meal id not does not exist, return -5, 404 
        '''

        (b, m) = mealColl.findMealID(id)
        if b:
            return m, 200  # return the meal and HTTP 200 ok code
        else:
            return -5, 404  # return -5 for key and Not Found error code

    def put(self, id):
        """ Modifies a meal associated with a specific ID

        :param id: the ID of the meal to be modified
        :return: the JSON object of the modified meal
        """

        # todo
        ''' successful put request returns 200
        modify or add a new meal
        '''

        # in the query_string, "?word=w" where w is the word to replace the existing word
        parser = reqparse.RequestParser()  # initialize parse
        parser.add_argument('id', location='args', required=True)
        args = parser.parse_args()  # parse arguments to dictionary
        modifiedMeal = args["id"]
        # replace the word in the collection
        b, w = mealColl.replaceMeal(id, modifiedMeal)
        if b:
            return w, 200  # return the word and HTTP 200 ok code
        else:
            return 0, 404  #return 0 for key and Not Found error code


class MealsName(Resource):
    """ Implements the REST operations for the /meals/{name} resource

    /meals/{name}
        GET (return the JSON object of the meal given the name)
        DELETE (delete a meal of the given name)
    """

    global mealColl

    def delete(self, name):
        """ Delete a meal from the collection based off its name

        :param name: the meal of the meal to delete
        :return: the deleted meal and the status code
        """


        # todo
        '''
        retur id of the meal deleted 
        if meal id not does not exist, return -5, 404 
        '''

        b, w = mealColl.delMealName(name)
        if b:
            return w, 200  # return deleted word and HTTP 200 ok code
        else:
            return 0, 404  # return 0 for key value (error) and Not Found error code

    def get(self, name):
        """ Retrieve a specific meal from the collection based off its ID

        :param id: the ID of the meal to retrieve
        :return: the meal and the status code
        """

        # todo
        ''' send id of the meal and receive back the json meal object
        if meal id not does not exist, return -5, 404 
        '''


        (b, w) = mealColl.findMealName(name)
        if b:
            return w, 200  # return the word and HTTP 200 ok code
        else:
            return 0, 404  # return 0 for key and Not Found error code