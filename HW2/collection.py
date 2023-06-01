import requests

class DishCollection:
    """ DishCollection stores the dishes and performs operations on them
        Each dish is stored in a dictionary with a unique numerical key called id,
        and a value of the following:
            dish name, calories, size (default 100g), sodium, suger
    """

    def __init__(self):
        # self.opNum is the number of insertDish operations performed
        self.opNum = 0

        # self.dishes is a dictionary of the form {key:dish} where key is an integer and dish is a JSON object
        self.dishes = {}

    def retrieveAllDishes(self):
        """
        Retrieve all dicts containing dishes insertDish
        :return: list of all dishes in the collection
        """
        print("DishCollection: retrieving all dishes:")
        dishes_list = [dish for dish in self.dishes.values()]
        print(dishes_list)

        return dishes_list

    def insertDish(self, dish_name):
        """
        Insert a new dish based on dish name
        param: dish_name
        return: id of the new dish (key) and status code
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

                    self.opNum += 1  # increment latest operation number

                    # Add dish to dish collection
                    self.dishes[self.opNum] = {
                        "name": dish_name,
                        "ID": self.opNum,
                        "cal": total_calories
                        "size": total_serving_size
                        "sodium": total_sodium
                        "sugar": total_sugar
                    }
                    print(self.dishes)
                    print("DishCollection: dish ", dish_name, " was added")

            else:
                print(f"Api Ninja/Nutrition not reachable: {response.status_code}, {response.text}")
                return -4
        except Exception as e:
            print(f"Api Ninja/Nutrition not reachable: {e}")
            return -4

        return self.opNum

    def findDishID(self, id):
        """
        Return a single JSON object of the dish specified by its ID
        :param id: the ID of the dish
        :return: JSON object of the dish
        """

        if id in self.dishes.keys():  # the id exists in collection
            d = self.dishes[id]
            print("DishCollection: found dish ", d, " with id ", id)
            return True, d
        else: # the id does not exist in the collection
            print("DishCollection: did not find id", id)
            return False, None

    def delDishID(self, id):

        if id in self.dishes.keys():  # the key exists in collection
            d = self.dishes[id]
            del self.dishes[id]
            print("DishCollection: deleted dish ", d, " with id ", id)
            return True, id

        else: # the key does not exist in the collection
            return False, None

    def delDishName(self, name):

        id_to_delete = None
        for id, dish in self.dishes.items():
            if dish["name"] == name:
                id_to_delete = id
                break

        # Delete dish from dictionary by key
        if id_to_delete is not None:
            del self.dishes[id_to_delete]
            print("DishCollection: deleted dish with name ", name)
            return True, id_to_delete
        else:
            print("DishCollection: did not find dish_name ", name)
            return False, None

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

    def checkDishes(self, list_of_ids):
        """
        Checks if all IDs in a list exist in dishes
        :params: list of dish IDs
        :return: True or False depending on results
        """

        exists = all(elem in self.dishes.keys() for elem in list_of_ids)
        print(f"All dishes exist: {exists}")
        return exists

class MealCollection:
    """ MealCollection stores the dishes and performs operations on them
        Each meal is stored in a dictionary with a unique numerical key called id,
        and a value of the following:
            name, ID, appetizer, main, dessert, cal, sodium, sugar
    """

    def __init__(self):
        # self.opNum is the number of insertMeal operations performed
        self.opNum = 0

        # self.meals is a dictionary of the form {key:meal} where key is an integer and meal is a list JSON objects
        self.meals = {}


    def retrieveAllMeals(self):
        """
        Retrieve all dicts containing meals
        :return: list of all meals in the collection
        """
        print("MealCollection: retrieving all meals:")
        meals_list = [meal for meal in self.meals.values()]
        print(meals_list)

        return meals_list

    def updateMeals(self, dish_id):
        """ Given a dish_id, update the meals

        :param dish_id: dish ID being deleted
        """

        for id, meal in self.meals.items(): # iterate over all dishes in a meal
            delete_components = False

            # null out the dish ID that was deleted and associated with the meal
            if dish_id == meal["appetizer"]:
                meal["appetizer"] = None
                delete_components = True
            elif dish_id == meal["main"]:
                meal["main"] = None
                delete_components = True
            elif dish_id["dessert"]:
                dish_id["dessert"] = None
                delete_components = True

            if delete_components: # if a dish ID was deleted, null out the components
                meal["cal"], meal["sodium"], meal["sugar"] = None, None, None

    def insertMeal(self, meal_name, appetizer_id, main_id, dessert_id, disheColl):
        """"
        Insert a meal given the name and the corresponding dish IDs. To create a meal, it
        computes the total numebr of calories, sodium, sugar.

        :param: meal name and component dish IDs
        :returns: the ID of the created meal
        """

        for id, meal in self.meals.items(): # check if meal exists, if so - return an error
            if meal["name"] == meal_name:
                print("MealCollection: meal ", meal_name, " already exists")
                return -2

        self.opNum += 1  # increment latest operation number

        self.meals[self.opNum] = { # sum over all components
            "name": meal_name,
            "ID": self.opNum,
            "appetizer": appetizer_id,
            "main": main_id,
            "dessert": dessert_id,
            "cal": sum(cal for cal in [disheColl.dishes[appetizer_id]["cal"], disheColl.dishes[main_id]["cal"], disheColl.dishes[dessert_id]["cal"]]),
            "sodium": sum(sodium for sodium in [disheColl.dishes[appetizer_id]["sodium"], disheColl.dishes[main_id]["sodium"], disheColl.dishes[dessert_id]["sodium"]]),
            "sugar": sum(sugar for sugar in [disheColl.dishes[appetizer_id]["sugar"], disheColl.dishes[main_id]["sugar"], disheColl.dishes[dessert_id]["sugar"]])
        }
        print("MealCollection: meal ", meal_name, " was added")

        return self.opNum

    def delMealID(self, id):
        """" Given a meal ID, delete it from the colleciton

        :params: the ID of a meal to delete
        :returns: True if successfully deleted, False if not found
        """

        if id in self.meals.keys():  # the key exists in collection
            d = self.meals[id]
            del self.meals[id]
            print("MealCollection: deleted meal ", d, " with id ", id)
            return True, d
        else:
            return False, None  # the key does not exist in the collection

    def findMealID(self, id):
        """ Given a meal ID, find the resulting collection

        :params: the ID of the meal to find
        :returns: True if found, False if not
        """
        if id in self.meals.keys():  # the key exists in collection
            d = self.meals[id]
            print("MealCollection: found meal ", d, " with id ", id)
            return True, d
        else:
            print("MealCollection: did not find id", id)
            return False, None  # the key does not exist in the collection

    def delMealName(self, name):
        """ Given a meal name, delete the meal

        :params: the name of the meal to delete
        :returns: True if successfully deleted (and its ID), False if not
        """

        id_to_delete = None
        for id, meal in self.meals.items(): #search for the meal ID given the name
            if meal["name"] == name:
                id_to_delete = id
                break

        # Delete dish from dictionary by key
        if id_to_delete is not None:
            del self.meals[id_to_delete]
            print("MealCollection: deleted meal with name ", name)
            return True, id_to_delete
        else:
            print("MealCollection: did not find meal_name ", name)
            return False, None

    def findMealName(self, name):
        """
         Returns a single JSON object of the meal specified by its name
         param name: the name of the meal
         return: value of the meal
         """

        fetch_id = None
        for id, meal in self.meals.items(): #search for the meal ID given the name
            if meal["name"] == name:
                fetch_id = id
                break

        if fetch_id is not None:  # Return meal from dictionary by key
            print("MealCollection: found meal ", self.meals[fetch_id], " with id ", fetch_id)
            return True, self.meals[fetch_id]
        else:
            print("MealCollection: did not find meal_name ", name)
            return False, None  # the key does not exist in the collection

    def replaceMeal(self, id, meal_name, appetizer_id, main_id, dessert_id, disheColl):
        """ Given a meal ID, replaces the meal components with the new meal name and component IDs

        :params: ID of meal to replace and new components (name and IDs)
        :returns: True if updated, False if meal was not in collection
        """

        if id in self.meals.keys():  # the key exists in collection
            self.meals[id] = {
                "name": meal_name,
                "ID": id,
                "appetizer": appetizer_id,
                "main": main_id,
                "dessert": dessert_id,
                "cal": sum(cal for cal in [disheColl.dishes[appetizer_id]["cal"], disheColl.dishes[main_id]["cal"],
                                           disheColl.dishes[dessert_id]["cal"]]),
                "sodium": sum(sodium for sodium in
                              [disheColl.dishes[appetizer_id]["sodium"], disheColl.dishes[main_id]["sodium"],
                               disheColl.dishes[dessert_id]["sodium"]]),
                "sugar": sum(sugar for sugar in
                             [disheColl.dishes[appetizer_id]["sugar"], disheColl.dishes[main_id]["sugar"],
                              disheColl.dishes[dessert_id]["sugar"]])
            }
            print("MealCollection: New meal for id ", id, " is ", self.meals[id])

            return True, self.meals[id]

        else:  # the key does not exist in the collection
            print("MealCollection: did not find id", id)
            return False, None
