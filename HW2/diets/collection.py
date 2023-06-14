# import pymongo
#
# client = pymongo.MongoClient("mongodb://mongo:27017/")  # Establish a connection to MongoDB
# db = client["nutrition"]                                # Access the "nutrition" database
# dietscoll = db["diets"]                                 # Access the "diets" collection
# result = dietscoll.insert_one({"_id":1, "value": "test - first value in diets DB"})
#
# # Print the inserted document
# print(result.inserted_id)
#
# # Retrieve all documents in the collection
# documents = dietscoll.find()
# for document in documents:
#     print(document)


class DietCollection:
    """ DietCollection stores the old and performs operations on them
    Each diet is stored in a dictionary with a unique numerical key called id,
    and a value of the following: name, cal, sodium, sugar
    """

    def __init__(self):
        self.opNum = 0
        self.diets = {}

        # client = pymongo.MongoClient("mongodb://mongo:27017/")   # Connect to the MongoDB server
        # db = client["nutrition"]                                 # Access the database
        #
        # # Check if the "diets" collection exists, create it if it doesn't
        # if "diets" not in db.list_collection_names():
        #     db.create_collection("diets")
        #
        # self.diets = db["diets"]    # Access the "diets" collection

        # keynum = self.diets.find_one(sort=[("_id", -1)])["_id"]
        # keynum +=1

    def retrieveAllDiets(self):
        """
        :return: list of all old in the collection, excluding the "ID" key
        """
        print("DietCollection: retrieving all old:")
        diets_list = []
        for diet in self.diets.values():
            diet_without_id = diet.copy()  # Create a copy of the diet object
            del diet_without_id["ID"]  # Remove the "ID" key from the copied object
            diets_list.append(diet_without_id)
        print(diets_list)
        return diets_list

    def insertDiet(self, diet_name, cal, sodium, sugar):
        """ Insert a new diet
        param: diet_name, cal, sodium, sugar
        return: id of the new diet (key) and status code
        """

        for id, diet in self.diets.items(): # check if diet exists, if so - return an error
            if diet["name"] == diet_name:
                print("Diet with name", diet_name, "already exists")
                return 0

        self.opNum += 1  # increment latest operation number

        self.diets[self.opNum] = {
            "name": diet_name,
            "ID": self.opNum,
            "cal": cal,
            "sodium": sodium,
            "sugar": sugar
        }
        print("Diet ", diet_name, " was created successfully")

        return self.opNum

    def findDietName(self, name):
        """
        param name: the name of the diet
        return: single JSON object of the diet specified by its name
        """

        fetch_id = None
        for id, diet in self.diets.items():
            if diet["name"] == name:
                fetch_id = id
                break

        if fetch_id is not None: # Return diet from dictionary by key
            print("DietCollection: found diet ", self.diets[fetch_id], " with id ", fetch_id)
            return True, self.diets[fetch_id]
        else:
            print(f"Diet {name} not found", name)
            return False, None  # the key does not exist in the collection
