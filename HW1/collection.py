import requests

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

    # COMPLETED
    def retrieveAllDishes(self):
        """
        Retrieve all dicts containing dishes
        :return: dictionary of all dishes in the collection
        """
        print("DishCollection: retrieving all dishes:")
        print(self.dishes)

        return self.dishes

    # COMPLETED
    def insertDish(self, dish_name):
        """
        Insert a new dish based on dish name
        param: dish_name
        return: id of the new dish (key) and status code
        """

        # Iterate over existing dishes collection and check if dish with same name already exists
        for id, dish in self.dishes.items():
            if dish["name"] == dish_name: # If dish already exists, returns an error
                print("DishCollection: dish ", dish_name, " already exists")
                return None

        self.opNum += 1 # increment latest operation number

        try:
            # Query API Ninja /nutrition
            api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(dish_name)
            response = requests.get(api_url, headers={'X-Api-Key': '6zoIr+IoEg7H2GQGVDxw+g==WdtcKEIt1DOIoGKj'})

            if response.status_code == requests.codes.ok: # Check status code of response
                json_data = response.json()
                for _dish in json_data:
                    self.dishes[self.opNum] = {
                        "name": dish_name,
                        "ID": self.opNum,
                        "cal": _dish["calories"],
                        "size": _dish["serving_size_g"],
                        "sodium": _dish["sodium_mg"],
                        "sugar": _dish["sugar_g"]
                    }
                    print(self.dishes)
                print("DishCollection: dish ", dish_name, " was added")
            else:
                print("Error with Api Ninja/Nutrition:", response.status_code, response.text)
                return -4
        except Exception as e:
            print(f"Api Ninja/Nutrition not reachable: {e}")
            return -4

        return self.opNum

    # COMPLETED
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
        else:
            print("DishCollection: did not find id", id)
            return False, None  # the id does not exist in the collection

    # COMPLETED
    def delDishID(self, id):

        if id in self.dishes.keys():  # the key exists in collection
            d = self.dishes[id]
            del self.dishes[id]
            print("DishCollection: deleted dish ", d, " with id ", id)
            return True, id
        else:
            return False, None  # the key does not exist in the collection

    # COMPLETED
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

    # COMPLETED
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


class MealCollection:
    """ MealCollection stores the dishes and performs operations on them
        Each meal is stored in a dictionary with a unique numerical key called id,
        and a value of the following:
            name, ID, appetizer, main, dessert, cal, sodium, sugar
    """

    def __init__(self):
        # self.opNum is the number of insertMeal operations performed so far.
        # It will be used to generate unique keys to meals inserted into the collection
        self.opNum = 0

        # self.meals is a dictionary of the form {key:meal} where key is an integer and meal is a list JSON objects
        self.meals = {}  # meals in the collection


    def retrieveAllMeals(self):
        """
        Retrieve all dicts containing meals
        :return: dictionary of all meals in the collection
        """
        print("MealCollection: retrieving all meals:")
        print(self.meals)

        # todo - make sure this is indexed by ID

        return self.meals

    def insertMeal(self, meal_name, appetizer_id, main_id, dessert_id, disheColl):

        '''
        when user creates a meal, the program needs to compute the total calories, sodium, sugar by summing
        those components for all the individual dishes that make up the meal
        - if meal gets updated, then those components needs to be updated as well
        '''

        for id, meal in self.meals.items():
            if meal["name"] == meal_name: # If meal already exists, returns an error
                print("MealCollection: meal ", meal_name, " already exists")
                return 0

        self.opNum += 1  # increment latest operation number
        key = self.opNum  # assign new key to new operation number

        self.meals[self.opNum] = {
            "name": meal_name,
            "ID": self.opNum,
            "appetizer": appetizer_id,
            "main": main_id,
            "dessert": dessert_id,
            "cal": sum(cal for cal in [disheColl.dishes[appetizer_id]["cal"], disheColl.dishes[main_id]["cal"], disheColl.dishes[dessert_id]["cal"]]),
            "sodium": sum(sodium for sodium in [disheColl.dishes[appetizer_id]["sodium"], disheColl.dishes[main_id]["sodium"], disheColl.dishes[dessert_id]["sodium"]]),
            "suger": sum(sugar for sugar in [disheColl.dishes[appetizer_id]["sugar"], disheColl.dishes[main_id]["sugar"], disheColl.dishes[dessert_id]["sugar"]])
        }
        print("MealCollection: meal ", meal_name, " was added")

        return self.opNum

    def delMealID(self, id):

        if id in self.meals.keys():  # the key exists in collection
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

        id_to_delete = None
        for id, meal in self.meals.items():
            if meals["name"] == name:
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
        for id, meal in self.meals.items():
            if dish["name"] == name:
                fetch_id = id
                break

        if fetch_id is not None:  # Return meal from dictionary by key
            print("MealCollection: found meal ", self.meals[fetch_id], " with id ", fetch_id)
            return True, self.meals[fetch_id]
        else:
            print("MealCollection: did not find meal_name ", name)
            return False, None  # the key does not exist in the collection


    def replaceMeal(self, id, newMeal):
        if id in self.meals.keys():  # the key exists in collection
            self.meals[id] = newMeal
            print("MealCollection: New meal for id ", id, " is ", newMeal)
            return True, newMeal
        else:  # the key does not exist in the collection
            print("MealCollection: did not find id", id)
            return False, None
