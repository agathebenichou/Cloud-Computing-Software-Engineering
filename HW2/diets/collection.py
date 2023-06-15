import pymongo

class DietCollection:
    """ DietCollection stores diets and performs operations on them
    The diets DB is a collection held in the "nutrition" database.
    Each diet document is stored with a unique numerical key called _id,
    and values of the following: name, cal, sodium, sugar
    """

    def __init__(self):

        client = pymongo.MongoClient("mongodb://mongo:27017/")   # Connect to the MongoDB server
        db = client["nutrition"]                                 # Access the database

        # Check if the "diets" collection exists, create it if it doesn't
        if "diets" not in db.list_collection_names():
            db.create_collection("diets")

        self.diets = db["diets"]    # Access the "diets" collection

        latest_diet_id = self.diets.find_one(sort=[("_id", -1)])
        if latest_diet_id is not None:
            self.opNum = latest_diet_id["_id"]
        else:
            self.opNum = 0

    def retrieveAllDiets(self):
        """
        :return: list of all old in the collection, excluding the "ID" key
        """
        print("DietCollection: retrieving all old:")
        diets_list = []

        cursor = self.diets.find()  # Retrieve all documents from the collection
        for diet in cursor:
            diet_without_id = diet.copy()
            del diet_without_id["_id"]
            diets_list.append(diet_without_id)
        print(diets_list)
        return diets_list

    def insertDiet(self, diet_name, cal, sodium, sugar):
        """ Insert a new diet
        param: diet_name, cal, sodium, sugar
        return: id of the new diet (key)
        """

        # Check if diet with the same name already exists in the collection
        existing_diet = self.diets.find_one({"name": diet_name})
        if existing_diet:
            print("Diet with name", diet_name, "already exists")  # Instructions are "Diet with <name> already exists", different to the screenshot, dont think it matters
            return 0

        self.opNum += 1  # increment latest operation number

        diet = {
            "name": diet_name,
            "cal": cal,
            "sodium": sodium,
            "sugar": sugar,
            "_id": self.opNum,
        }

        # Insert the new diet document into the collection
        result = self.diets.insert_one(diet)
        if result.inserted_id:
            print("Diet", diet_name, "was created successfully")
        return self.opNum


    def findDietName(self, name):
        """
        param name: the name of the diet
        return: Boolean if diet was found and BSON object of the diet specified by its name
        """

        diet = self.diets.find_one({"name": name})  # Find the diet by name in the collection

        if diet is not None:
            del diet["_id"]
            return True, diet
        else:
            return False, None
