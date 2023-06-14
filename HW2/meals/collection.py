import requests
import pymongo


class DishCollection:
    """ DishCollection stores the dishes and performs operations on them
        Each dish is stored in a dictionary with a unique numerical key called id,
        and a value of the following: dish name, calories, size (default 100g), sodium, suger
    """

    def __init__(self):

        client = pymongo.MongoClient("mongodb://mongo:27017/")   # Connect to the MongoDB server
        db = client["nutrition"]                                 # Access the database

        # Check if the "dishes" collection exists, create it if it doesn't
        if "diets" not in db.list_collection_names():
            db.create_collection("dishes")

        self.dishes = db["dishes"]    # Access the "dishes" collection

        latest_dish_id = self.dishes.find_one(sort=[("_id", -1)])
        if latest_dish_id is not None:
            self.opNum = latest_dish_id["_id"]
        else:
            self.opNum = 0


    def retrieveAllDishes(self):
        """
        Retrieve all dishes
        :return: list of all dishes in the collection
        """

        print("DishCollection: retrieving all dishes:")
        dishes_list = []

        cursor = self.dishes.find()  # Retrieve all documents from the collection
        for dish in cursor:
            dish_without_id = dish.copy()
            del dish_without_id["_id"]
            dishes_list.append(dish_without_id)

        print(dishes_list)
        return dishes_list


    def insertDish(self, dish_name):
        """
        Insert a new dish based on dish name, using API Ninja/Nutrition
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
        """
        Return a single BSON object of the dish specified by its ID
        :param id: the ID of the dish
        :return: BSON object of the dish
        """

        dish = self.dishes.find_one({"ID": id})
        if dish:
            print("DishCollection: found dish", dish, "with ID", id)
            return True, dish

        print("DishCollection: did not find ID", id)
        return False, None

    def findDishName(self, name):
        """
        Return a single BSON object of the dish specified by its name
        param name: the name of the dish
        return: BSON object of the dish
        """


        dish = self.dishes.find_one({"name": name})
        if dish:
            print("DishCollection: found dish", dish, "with name", name)
            return True, dish

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

        result = self.dishes.delete_many({"name": name})
        if result.deleted_count > 0:
            print("DishCollection: deleted dish with name", name)
            return True, result.deleted_count

        return False, None

    def checkDishes(self, list_of_ids):
        """
        Checks if all IDs in a list exist in dishes
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
        self.opNum = 0
        self.meals = []

    def retrieveAllMeals(self):
        """
        Retrieve all dicts containing meals
        :return: list of all meals in the collection
        """
        print("MealCollection: retrieving all meals:")
        meals_list = [meal for meal in self.meals]
        print(meals_list)

        return meals_list

    def updateMeals(self, dish_id):
        """ Given a dish_id, update the meals
        :param dish_id: dish ID being deleted
        """

        for meal in self.meals:
            delete_components = False

            # null out the dish ID that was deleted and associated with the meal
            if dish_id == meal["appetizer"]:
                meal["appetizer"] = None
                delete_components = True
            elif dish_id == meal["main"]:
                meal["main"] = None
                delete_components = True
            elif dish_id == meal["dessert"]:
                meal["dessert"] = None
                delete_components = True

            if delete_components: # if a dish ID was deleted, null out the components
                meal["cal"], meal["sodium"], meal["sugar"] = None, None, None

    def insertMeal(self, meal_name, appetizer_id, main_id, dessert_id, disheColl):
        """ Insert a meal given the name and the corresponding dish IDs. To create a meal, it
        computes the total number of calories, sodium, sugar.

        :param: meal name and component dish IDs
        :returns: the ID of the created meal
        """

        for meal in self.meals:
            print(meal)
            if meal["name"] == meal_name:
                print("MealCollection: meal ", meal_name, " already exists")
                return -2

        self.opNum += 1  # increment latest operation number

        self.meals.append(
            {
                "name": meal_name,
                "ID": self.opNum,
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
                )
            }
        )
        print("MealCollection: meal ", meal_name, " was added")

        return self.opNum

    def delMealID(self, id):
        """" Given a meal ID, delete it from the collection

        :params: the ID of a meal to delete
        :returns: True if successfully deleted, False if not found
        """
        for meal in self.meals:
            if id == meal["ID"]:
                self.meals.remove(meal)
                print("MealCollection: deleted meal with id ", id)
                return True, id

        return False, None  # the key does not exist in the collection

    def delMealName(self, name):
        """ Given a meal name, delete the meal

        :params: the name of the meal to delete
        :returns: True if successfully deleted (and its ID), False if not
        """

        for meal in self.meals:
            if name == meal["name"]:
                id_deleted = meal["ID"]
                self.meals.remove(meal)
                print("MealCollection: deleted meal with name ", name)
                return True, id_deleted

        return False, None  # the key does not exist in the collection

    def findMealID(self, id):
        """ Given a meal ID, find the resulting collection

        :params: the ID of the meal to find
        :returns: True if found, False if not
        """

        for meal in self.meals:
            if id == meal["ID"]:
                print("MealCollection: found meal ", meal, " with id ", id)
                return True, meal

        print("MealCollection: did not find id", id)
        return False, None  # the key does not exist in the collection

    def findMealName(self, name):
        """ Returns a single JSON object of the meal specified by its name
         param name: the name of the meal
         return: value of the meal
        """

        for meal in self.meals:
            if name == meal["name"]:
                print("MealCollection: found meal ", meal, " with name ", name)
                return True, meal

        print("MealCollection: did not find name", name)
        return False, None  # the key does not exist in the collection

    def replaceMeal(self, id, meal_name, appetizer_id, main_id, dessert_id, disheColl):
        """ Given a meal ID, replaces the meal components with the new meal name and component IDs

        :params: ID of meal to replace and new components (name and IDs)
        :returns: True if updated, False if meal was not in collection
        """

        for meal in self.meals:
            if id == meal["ID"]:

                # Delete old meal
                self.meals.remove(meal)

                # Replace with updated meal
                self.meals.append(
                    {
                        "name": meal_name,
                        "ID": id,
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
                        )
                    }
                )

                print(f"MealCollection: New meal {meal_name} added as ID={id}")
                return True, id

        # the key does not exist in the collection
        print("MealCollection: did not find id", id)
        return False, None
