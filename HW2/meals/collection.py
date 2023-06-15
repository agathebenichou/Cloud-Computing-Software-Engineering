import requests
import pymongo


class DishCollection:
    """ DishCollection stores the dishes and performs operations on them
    Each dish is stored in a dictionary with a unique numerical key called id,
    and a value of the following: dish name, calories, size (default 100g), sodium, suger
    """

    def __init__(self):
        """ Initialize the connection to the MongoDB server and access the database
        Extract the dishes collection and find latest ID
        """

        client = pymongo.MongoClient("mongodb://mongo:27017/")   # Connect to the MongoDB server
        db = client["nutrition"]                                 # Access the database

        # Check if the "dishes" collection exists, create it if it doesn't
        if "dishes" not in db.list_collection_names():
            db.create_collection("dishes")

        self.dishes = db["dishes"]    # Access the "dishes" collection

        # Extract the dish with the highest ID value (most recently inserted)
        latest_dish_id = self.dishes.find_one(sort=[("ID", -1)])
        if latest_dish_id is not None:
            self.opNum = latest_dish_id["ID"]
        else: # Initialize to 0 if there are no dishes
            self.opNum = 0

    def retrieveAllDishes(self):
        """ Retrieve all dishes
        :return: list of all dishes in the collection
        """

        print("DishCollection: retrieving all dishes:")
        dishes_list = []

        cursor = self.dishes.find()  # Retrieve all documents from the collection
        for dish in cursor:
            dish_copy = dish.copy()
            del dish_copy["_id"] # Remove the internal Mongo ID
            dishes_list.append(dish_copy)

        print(dishes_list)
        return dishes_list

    def insertDish(self, dish_name):
        """ Insert a new dish based on dish name, using API Ninja/Nutrition
        param: dish_name
        return: ID of the new dish
        """

        # Check if dish with the same name already exists
        dish_exists = self.dishes.find_one({"name": dish_name})
        if dish_exists:
            print("DishCollection: dish", dish_name, "already exists")
            return -2

        try:
            # Query API Ninja /nutrition
            api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(dish_name)
            response = requests.get(api_url, headers={'X-Api-Key': '6zoIr+IoEg7H2GQGVDxw+g==WdtcKEIt1DOIoGKj'})

            if response.status_code == requests.codes.ok:  # Check status code of response
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
                    dish = {
                        "name": dish_name,
                        "cal": total_calories,
                        "size": total_serving_size,
                        "sodium": total_sodium,
                        "sugar": total_sugar,
                        "ID": self.opNum,
                        "_id": self.opNum
                    }
                    self.dishes.insert_one(dish)
                    print("DishCollection: dish", dish_name, "was added")

            else:
                print(f"Api Ninja/Nutrition not reachable: {response.status_code}, {response.text}")
                return -4
        except Exception as e:
            print(f"Api Ninja/Nutrition not reachable: {e}")
            return -4

        return self.opNum

    def findDishID(self, id):
        """ Return a single BSON object of the dish specified by its ID
        :param id: the ID of the dish
        :return: JSON object of the dish
        """

        dish = self.dishes.find_one({"ID": id})
        if dish:
            dish_copy = dish.copy()
            del dish_copy["_id"]  # Remove the internal Mongo ID
            print("DishCollection: found dish", dish_copy, "with ID", id)
            return True, dish_copy

        print("DishCollection: did not find ID", id)
        return False, None

    def findDishName(self, name):
        """ Return a single BSON object of the dish specified by its name
        param name: the name of the dish
        return: BSON object of the dish
        """

        dish = self.dishes.find_one({"name": name})
        if dish:
            dish_copy = dish.copy()
            del dish_copy["_id"]  # Remove the internal Mongo ID
            print("DishCollection: found dish", dish_copy, "with name", name)
            return True, dish_copy

        print("DishCollection: did not find name", name)
        return False, None

    def delDishID(self, id):
        """ Deletes a dish with the corresponding ID
        :param id: dish ID to delete
        :return: True if deleted, False if not found
        """

        result = self.dishes.delete_one({"ID": id})
        if result.deleted_count > 0:
            print("DishCollection: deleted dish with ID", id)
            return True, id

        return False, None

    def delDishName(self, name):
        """ Deletes a dish with the corresponding name
        :param name: dish name to delete
        :return: True if deleted, False if not found
        """

        dish_to_delete = self.dishes.find_one({"name": name})

        if dish_to_delete:
            dish_to_delete_id = dish_to_delete["ID"]
            result = self.dishes.delete_one({"name": name})
            if result.deleted_count > 0:
                print("DishCollection: deleted dish with name", name)
                return True, dish_to_delete_id

        return False, None

    def checkDishes(self, list_of_ids):
        """ Checks if all IDs in a list exist in dishes
        :params: list of dish IDs
        :return: True or False depending on results
        """

        dish_ids_that_exist = [dish['ID'] for dish in self.dishes.find()]  # Retrieve IDs of existing dishes
        print(f"Dishes that exist: {dish_ids_that_exist}")
        print(f"Dishes IDs needed to create: {list_of_ids}")

        exists = all(elem in dish_ids_that_exist for elem in list_of_ids)
        print(f"All dishes exist: {exists}")
        return exists

    def extract_value(self, id, field):
        """ Given the ID of a dish and the field to extract, return the value """

        dish = self.dishes.find_one({"ID": id})  # Retrieve the dish document with the specified ID
        if dish:
            return dish.get(field)  # Return the value of the specified field
        return None


class MealCollection:
    """ MealCollection stores the dishes and performs operations on them
    Each meal is stored in a dictionary with a unique numerical key called id,
    and a value of the following: name, ID, appetizer, main, dessert, cal, sodium, sugar
    """

    def __init__(self):
        """ Initialize the connection to the MongoDB server and access the database
        Extract the meals collection and find latest ID
        """

        client = pymongo.MongoClient("mongodb://mongo:27017/")  # Connect to the MongoDB server
        db = client["nutrition"]  # Access the database

        # Check if the "meals" collection exists, create it if it doesn't
        if "meals" not in db.list_collection_names():
            db.create_collection("meals")

        self.meals = db["meals"]  # Access the "meals" collection

        # Extract the meal with the highest ID value (most recently inserted)
        latest_meal_id = self.meals.find_one(sort=[("ID", -1)])
        if latest_meal_id is not None:
            self.opNum = latest_meal_id["ID"]
        else:  # Initialize to 0 if there are no meals
            self.opNum = 0

    def retrieveAllMeals(self):
        """ Retrieve all dicts containing meals
        :return: list of all meals in the collection
        """

        print("MealCollection: retrieving all meals:")

        meals_list = []
        cursor = self.meals.find()  # Retrieve all documents from the collection
        for meal in cursor:
            meal_copy = meal.copy()
            del meal_copy["_id"]  # Remove internal Mongo ID
            meals_list.append(meal_copy)

        print(meals_list)
        return meals_list

    def updateMeals(self, dish_id):
        """ Given a dish_id, update the meals
        :param dish_id: dish ID being deleted
        """

        cursor = self.meals.find()  # Retrieve all documents from the collection
        for meal in cursor:
            delete_components = False

            # null out the dish ID that was deleted and associated with the meal
            if dish_id == meal["appetizer"]:
                meal["appetizer"] = None
                delete_components = True
            if dish_id == meal["main"]:
                meal["main"] = None
                delete_components = True
            if dish_id == meal["dessert"]:
                meal["dessert"] = None
                delete_components = True

            if delete_components: # if a dish was deleted, null out the components
                meal["cal"], meal["sodium"], meal["sugar"] = None, None, None
                self.meals.update_one({'_id': meal['_id']}, {'$set': meal})

    def insertMeal(self, meal_name, appetizer_id, main_id, dessert_id, disheColl):
        """ Insert a meal given the name and the corresponding dish IDs. To create a meal, it
        computes the total number of calories, sodium, sugar.
        :param: meal name and component dish IDs
        :returns: the ID of the created meal
        """

        # Check if dish with the same name already exists
        meal_exists = self.meals.find_one({"name": meal_name})
        if meal_exists:
            print("MealCollection: meal", meal_name, "already exists")
            return -2

        self.opNum += 1  # increment latest operation number

        meal = {
            "name": meal_name,
            "appetizer": appetizer_id,
            "main": main_id,
            "dessert": dessert_id,
            "cal": sum(
                cal for cal in [
                    disheColl.extract_value(id=appetizer_id, field="cal"),
                    disheColl.extract_value(id=main_id, field="cal"),
                    disheColl.extract_value(id=dessert_id, field="cal")
                ]
            ),
            "sodium": sum(
                sodium for sodium in [
                    disheColl.extract_value(id=appetizer_id, field="sodium"),
                    disheColl.extract_value(id=main_id, field="sodium"),
                    disheColl.extract_value(id=dessert_id, field="sodium")
                ]
            ),
            "sugar": sum(
                sugar for sugar in [
                    disheColl.extract_value(id=appetizer_id, field="sugar"),
                    disheColl.extract_value(id=main_id, field="sugar"),
                    disheColl.extract_value(id=dessert_id, field="sugar")
                ]
            ),
            "ID": self.opNum,
            "_id": self.opNum,
        }
        self.meals.insert_one(meal)
        print("MealCollection: meal ", meal_name, " was added")

        return self.opNum

    def delMealID(self, id):
        """ Given a meal ID, delete it from the collection
        :params: the ID of a meal to delete
        :returns: True if successfully deleted, False if not found
        """

        result = self.meals.delete_one({"ID": id})
        if result.deleted_count > 0:
            print("MealCollection: deleted meal with id ", id)
            return True, id

        return False, None  # the key does not exist in the collection

    def delMealName(self, name):
        """ Given a meal name, delete the meal
        :params: the name of the meal to delete
        :returns: True if successfully deleted (and its ID), False if not
        """

        meal_to_delete = self.meals.find_one({"name": name})

        if meal_to_delete:
            meal_to_delete_id = meal_to_delete["ID"]
            result = self.meals.delete_one({"name": name})
            if result.deleted_count > 0:
                print("MealCollection: deleted meal with name", name)
                return True, meal_to_delete_id

        return False, None  # the key does not exist in the collection

    def findMealID(self, id):
        """ Given a meal ID, find the resulting collection
        :params: the ID of the meal to find
        :returns: True if found, False if not
        """

        meal = self.meals.find_one({"ID": id})
        if meal:
            meal_copy = meal.copy()
            del meal_copy["_id"]  # Remove the internal Mongo ID
            print("MealCollection: found dish", meal_copy, "with ID", id)
            return True, meal_copy

        print("DishCollection: did not find ID", id)
        return False, None

    def findMealName(self, name):
        """ Returns a single JSON object of the meal specified by its name
        :params: the name of the meal
        :returns: value of the meal
        """

        meal = self.meals.find_one({"name": name})
        if meal:
            meal_copy = meal.copy()
            del meal_copy["_id"]  # Remove the internal Mongo ID
            print("MealCollection: found dish", meal_copy, "with name", name)
            return True, meal_copy

        print("MealCollection: did not find name", name)
        return False, None

    def replaceMeal(self, id, meal_name, appetizer_id, main_id, dessert_id, disheColl):
        """ Given a meal ID, replaces the meal components with the new meal name and component IDs
        :params: ID of meal to replace and new components (name and IDs)
        :returns: True if updated, False if meal was not in collection
        """

        cursor = self.meals.find()  # Retrieve all documents from the collection
        for meal in cursor:
            if id == meal["ID"]:

                # Delete old meal
                self.meals.delete_one({"ID": id})

                updated_meal = {
                    "name": meal_name,
                    "appetizer": appetizer_id,
                    "main": main_id,
                    "dessert": dessert_id,
                    "cal": sum(
                        cal for cal in [
                            disheColl.extract_value(id=appetizer_id, field="cal"),
                            disheColl.extract_value(id=main_id, field="cal"),
                            disheColl.extract_value(id=dessert_id, field="cal")
                        ]
                    ),
                    "sodium": sum(
                        sodium for sodium in [
                            disheColl.extract_value(id=appetizer_id, field="sodium"),
                            disheColl.extract_value(id=main_id, field="sodium"),
                            disheColl.extract_value(id=dessert_id, field="sodium")
                        ]
                    ),
                    "sugar": sum(
                        sugar for sugar in [
                            disheColl.extract_value(id=appetizer_id, field="sugar"),
                            disheColl.extract_value(id=main_id, field="sugar"),
                            disheColl.extract_value(id=dessert_id, field="sugar")
                        ]
                    ),
                    "ID": id,
                    "_id": id,
                }

                # Replace with updated meal
                self.meals.insert_one(updated_meal)

                print(f"MealCollection: meal {meal_name} with ID={id} was updated")
                return True, id

        # the key does not exist in the collection
        print("MealCollection: did not find id", id)
        return False, None
