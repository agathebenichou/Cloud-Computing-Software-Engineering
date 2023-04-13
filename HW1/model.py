from flask_restful import Resource, reqparse
from collection import DishCollection, MealCollection

"""
The resources are:

- /meals                            This is a collection class, containing all the meals
- /meals/{ID} or /meals/{name}      Each meal resource is expressed with a specific JSON object
- /dishes                           This is a collection class, containing all the dishes 
- /dishes/{ID} or /dishes/{name}    Each dish resource is expressed with a specific JSON object
"""

# todo  - check all functioanlity against requirements in powerpoint

# create DishCollection instance with global scope
dishColl = DishCollection()


class Dishes(Resource):
    """ The Dishes class implements the REST operations for the /dishes resource

    /dishes
        POST (add a dish of the given name)
        GET (return the JSON object listing all dishes, indexed by ID)
    """

    global dishColl

    def get(self):
        """ Retrieves a specific dish from the collection

        :param key: the key used to search for a dish (either ID or name)
        :return: JSON object listing all dishes (indexed by ID) and the status code
        """

        return dishColl.retrieveAllDishes(), 200

    def post(self):
        """ Adds a dish to /dishes

        :param key: name used to add a dish
        :return: id: dish ID given to the dish
        """

        # get argument being passed in query string
        parser = reqparse.RequestParser()  # initialize parse

        # in the query_string, expect "?name=d" where d is the name of the dish to be added
        parser.add_argument('name', location='args', required=True)
        args = parser.parse_args()  # parse arguments into a dictionary structure
        d = args["name"]

        # add d to collection
        id = dishColl.insertDish(d)

        # todo - if successful,returns dish ID, a positive integeer and the 201 code
        # todo - if not, return non pos ID (0, -1, -2, -3, -4) slide number 9
        '''
        • 0 means that request content-type is not application/json. Status code 415 (Unsupported Media Type)
        • -1 means that 'name' parameter was not specified in the message body. Status code 422
        (Unprocessable Content)
        • -2 means that dish of given name already exists. Status code 422 (Unprocessable Content)
        • -3 means that api.api-ninjas.com/v1/nutrition does not recognize this dish name. Status code 422
        (Unprocessable Content)
        • -4 means that api.api-ninjas.com/v1/nutrition was not reachable. Status code 504 (Gateway Timeout)
        '''
        if id == 0:   # word already exists
            return id, 422
        return id, 201

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

    def get(self, id):
        """ Retrieve a specific dish from the collection based off its ID

        :param id: the ID of the dish to retrieve
        :return: the dish JSON object and the status code
        """

        # todo - if dish id does not esist, return -5 with status code 404
        (b, d) = dishColl.findDishID(id)
        if b:
            return d, 200  # return the word and HTTP 200 ok code
        else:
            return 0, 404  # return 0 for key and Not Found error code

    def delete(self, id):
        """ Delete a dish from the collection based off its ID

        :param id: the ID of the dish to delete
        :return: the deleted dish ID and the status code
        """

        # todo - if dish id does not esist, return -5 with status code 404

        b, d = dishColl.delDishID(id)
        if b:
            return id, 200  # return deleted dosj and HTTP 200 ok code
        else:
            return 0, 404  # return 0 for id value (error) and Not Found error code


class DishesName(Resource):
    """ Implements the REST operations for the /dishes/{name} resource

    /dishes/{name}
        GET (return the JSON object of the dish given the name)
        DELETE (delete a dish of the given name)
    """

    global dishColl

    def delete(self, name):
        """ Delete a dish from the collection based off its name

        :param name: the ma,e of the dish to delete
        :return: the deleted dish and the status code
        """
        # todo - if dish name does not esist, return -5 with status code 404
        b, w = dishColl.delDishName(name)
        if b:
            return name, 200  # return deleted word and HTTP 200 ok code
        else:
            return 0, 404  # return 0 for key value (error) and Not Found error code

    def get(self, name):
        """ Retrieve a specific dish from the collection based off its ID

        :param id: the ID of the dish to retrieve
        :return: the dish and the status code
        """
        # todo - if dish id does not esist, return -5 with status code 404
        (b, w) = dishColl.findDishName(name)
        if b:
            return name, 200  # return the word and HTTP 200 ok code
        else:
            return 0, 404  # return 0 for key and Not Found error code


# create MealCollection instance with global scope
mealColl = MealCollection()


class Meals(Resource):
    """ The Meal class implements the REST operations for the /meals resource

    /meals
        POST (add a meal of the given name)
        GET (return the JSON object listing all meals, indexed by ID)
    """

    global mealColl

    def get(self):
        """ Retrieves a specific meal from the collection

        :return: all meal objects and status code
        """

        return mealColl.retrieveAllMeals(), 200

    def post(self):
        """ Adds a meal to /meals

        :param key: name used to add a meal
        :return: id: ID given to the meal
        """

        # get argument being passed in query string
        parser = reqparse.RequestParser()  # initialize parse

        # todo
        '''
        post will be a dict of {name, appretizer, main, dessert}
        need to parse dict and pass components (or pass componens and parse in collection)
        PASSES DISH IDs, not names
        if incorrect / doesnt exist dish id, return -5, 422
        '''

        # in the query_string, expect "?name=m" where m is the name of the meal to be added
        parser.add_argument('name', location='args', required=True)
        args = parser.parse_args()  # parse arguments into a dictionary structure
        m = args["name"]

        # todo
        '''
        POST can retur a non positve ID with the following meaning:
        0 means that request content-type is not application/json. Status code 415 (Unsupported Media Type)
        -1 means that one of the required parameters was not given or not specified correctly. Status code 422
        (Unprocessable Entity)
        -2 means that a meal of the given name already exists. Status code 422 (Unprocessable Entity)
        -6 means that one of the sent dish IDs (appetizer, main, dessert) does not exist. Status code 422
        (Unprocessable Entity)* 
        '''

        # add d to collection
        key = mealColl.insertMeal(m)
        if key == 0:  # word already exists
            return key, 422
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
        """ Retrieve a specific meal from the collection based off its ID

        :param id: the ID of the meal to retrieve
        :return: the meal and the status code
        """

        # todo
        ''' send id of the meal and receive back the json meal object
        if meal id not does not exist, return -5, 404 
        '''

        (b, w) = mealColl.findMealID(id)
        if b:
            return w, 200  # return the meal and HTTP 200 ok code
        else:
            return 0, 404  # return 0 for key and Not Found error code

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