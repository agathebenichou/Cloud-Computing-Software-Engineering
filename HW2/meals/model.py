import requests
from flask import request
from flask_restful import Resource
from .collection import DishCollection, MealCollection

"""
The resources are:

- /meals                            This is a collection class, containing all the meals
- /meals/{ID} or /meals/{name}      Each meal resource is expressed with a specific JSON object
- /dishes                           This is a collection class, containing all the dishes 
- /dishes/{ID} or /dishes/{name}    Each dish resource is expressed with a specific JSON object
- /diets or /diets/{name}            Each diet resource is expressed with a specific JSON object
"""

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

        # if request content-type is not application/json
        if 'Content-Type' not in dict(request.headers).keys():
            print("Request Content-Type not specified in header")
            return 0, 415
        else:
            if dict(request.headers)['Content-Type'] != "application/json":
                print("Request Content-Type is not application/json")
                return 0, 415

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

        id = dishColl.insertDish(d)  # add d to collection

        if id == -2:   # dish already exists
            return id, 422
        elif id == -3:  # api.api-ninjas.com/v1/nutrition does not recognize dish name
            return id, 422
        elif id == -4:  # api.api-ninjas.com/v1/nutrition was not reachable
            return -4, 504
        return id, 201

    def delete(self):
        """ Deleting the entire collection is not allowed
        :return: return error message
        """

        return "This method is not allowed for the requested URL", 405


class DishesID(Resource):
    """ Implements the REST operations for the /dishes/{ID} resource

    /dishes/{ID}
        GET (return the JSON object of the dish given the ID)
        DELETE (delete a dish of the given ID)
    """

    global dishColl
    global mealColl

    def get(self, id):
        """ Retrieve a specific dish from the collection based off its ID

        :param id: the ID of the dish to retrieve
        :return: the dish JSON object and the status code
        """

        (status, dish_obj) = dishColl.findDishID(id)
        if status: # return the word and HTTP 200 ok code
            return dish_obj, 200
        else: # if dish not found
            return -5, 404

    def delete(self, id):
        """ Delete a dish from the collection based off its ID

        :param id: the ID of the dish to delete
        :return: the deleted dish ID and the status code
        """

        (status, dish_id) = dishColl.delDishID(id)
        if status: # return deleted dish and HTTP 200 ok code

            # update all meals to delete dish ID
            mealColl.updateMeals(dish_id)

            return dish_id, 200
        else: # return 0 for id value (error) and Not Found error code
            return -5, 404


class DishesName(Resource):
    """ Implements the REST operations for the /dishes/{name} resource

    /dishes/{name}
        GET (return the JSON object of the dish given the name)
        DELETE (delete a dish of the given name)
    """

    global dishColl
    global mealColl

    def delete(self, name):
        """ Delete a dish from the collection based off its name

        :param name: the nsmr of the dish to delete
        :return: the deleted dish and the status code
        """

        (status, dish_id) = dishColl.delDishName(name)
        if status: # return deleted word and HTTP 200 ok code

            # Update meal based off of
            mealColl.updateMeals(dish_id)

            return dish_id, 200
        else: # return 0 for key value (error) and Not Found error code
            return -5, 404

    def get(self, name):
        """ Retrieve a specific dish from the collection based off its ID

        :param name: the name of the dish to retrieve
        :return: the dish and the status code
        """

        (status, dish_obj) = dishColl.findDishName(name)
        if status: # return the word and HTTP 200 ok code
            return dish_obj, 200
        else: # return 0 for key and Not Found error code
            return -5, 404


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
        """ Retrieves meals from the collection:
        If query is specified - return all meals corresponding to that diet
        Otherwise - return all meals
        """

        diet_name = request.args.get('diet')
        if diet_name:

            print(f"searching for diet name {diet_name}")

            # Define diets url with diet name
            diets_service_url = f"http://diet-service:5002/diets/{diet_name}"

            # Send GET request to diets service
            diet_response = requests.get(diets_service_url)

            # If the diet exists, extract and filter for meals
            if diet_response.status_code == 200:

                diet = diet_response.json()
                filtered_meals = []
                for meal in mealColl.meals:
                    if (meal['cal'] <= diet['cal'] and meal['sodium'] <= diet['sodium'] and meal['sugar'] <= diet['sugar']):
                        filtered_meals.append(meal)
                return filtered_meals, 200

            # No diet of that name exists
            else:
                return f"Diet {diet_name} not found", 404

        # Return all meals if no diet was specified
        else:
            return mealColl.retrieveAllMeals(), 200

    def post(self):
        """
        Adds a meal to /meals given a JSON object with fields: name, appetizer, main, dessert
        :return: id: ID given to the created meal
        """

        # if request content-type is not application/json
        if 'Content-Type' not in dict(request.headers).keys():
            print("Request Content-Type not specified in header")
            return 0, 415
        else:
            if dict(request.headers)['Content-Type'] != "application/json":
                print("Request Content-Type is not application/json")
                return 0, 415

        data = request.json

        # if body is not of type dict
        if type(data) != dict:
            return 0, 415
        else:

            # not all keys are present
            keys = ['name', 'appetizer', 'main', 'dessert']
            all_present = all(elem in data.keys() for elem in keys)

            if all_present:
                meal_name = data['name']
                appetizer_id = data['appetizer']
                main_id = data['main']
                dessert_id = data['dessert']
            else:
                return -1, 422

        dishes_exists = dishColl.checkDishes([appetizer_id, main_id, dessert_id])
        if dishes_exists:

            # add meal to collection (after check for dish existence)
            key = mealColl.insertMeal(meal_name, appetizer_id, main_id, dessert_id, dishColl)
            if key == -2:  # meal already exists
                return -2, 422
            return key, 201

        else:  # one of the dish IDs does not exist
            return -6, 422


class MealsID(Resource):
    """ Implements the REST operations for the /meals/{ID} resource

    /meals/{ID}
        GET (return the JSON object of the meal given the ID)
        DELETE (delete a meal of the given ID)
        PUT (add a meal of the given ID)
    """

    global mealColl
    global dishColl

    def delete(self, id):
        """ Delete a meal from the collection based off its ID

        :param id: the ID of the meal to delete
        :return: the deleted meal and the status code
        """
        b, w = mealColl.delMealID(id)
        if b:
            return w, 200  # return deleted meal ID and HTTP 200 ok code
        else:
            return -5, 404  # if not found

    def get(self, id):
        """
        Retrieve a specific meal from the collection based off its ID
        :param id: the ID of the meal to retrieve
        :return: the meal and the status code
        """

        (b, m) = mealColl.findMealID(id)
        if b:  # return the meal and HTTP 200 ok code
            return m, 200
        else:  # return -5 for key and Not Found error code
            return -5, 404

    def put(self, id):
        """ Modifies a meal associated with a specific ID

        :param id: the ID of the meal to be modified
        :return: the JSON object of the modified meal
        """

        # if request content-type is not application/json
        if 'Content-Type' not in dict(request.headers).keys():
            print("Request Content-Type not specified in header")
            return 0, 415
        else:
            if dict(request.headers)['Content-Type'] != "application/json":
                print("Request Content-Type is not application/json")
                return 0, 415

        data = request.json

        # if body is not of type dict
        if type(data) != dict:
            return 0, 415
        else:

            # not all keys are present
            keys = ['name', 'appetizer', 'main', 'dessert']
            all_present = all(elem in keys for elem in data.keys())

            if not all_present:
                print(f"One of the required parameters was not specified")
                return -1, 422
            else:
                meal_name = data['name']
                appetizer_id = data['appetizer']
                main_id = data['main']
                dessert_id = data['dessert']

        dishes_exists = dishColl.checkDishes([appetizer_id, main_id, dessert_id])
        if dishes_exists:

            # replace the word in the collection
            b, w = mealColl.replaceMeal(id, meal_name, appetizer_id, main_id, dessert_id, dishColl)
            if b: # return the word and HTTP 200 ok code
                return w, 200

            else: #return 0 for key and Not Found error code
                return -5, 404

        else:  # one of the dish IDs does not exist
            return -6, 422


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

        b, w = mealColl.delMealName(name)
        if b:
            return w, 200  # return deleted word and HTTP 200 ok code
        else:
            return -5, 404  # return 0 for key value (error) and Not Found error code

    def get(self, name):
        """ Retrieve a specific meal from the collection based off its ID

        :param id: the ID of the meal to retrieve
        :return: the meal and the status code
        """

        (b, w) = mealColl.findMealName(name)
        if b:
            return w, 200  # return the word and HTTP 200 ok code
        else:
            return -5, 404  # return 0 for key and Not Found error code