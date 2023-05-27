from flask import request
from flask_restful import Resource

class DietCollection:
    """ DietCollection stores the diets and performs operations on them
        Each diet is stored in a dictionary with a unique numerical key called id,
        and a value of the following:
            name, cal, sodium, sugar
    """

    def __init__(self):
        # self.opNum is the number of insertDiet operations performed, it also serves as the id for each diet
        self.opNum = 0

        # self.diets is a dictionary of the form {key:diet} where key is an integer and diet is a JSON object
        self.diets = {}

    def retrieveAllDiets(self):
        """
        :return: list of all diets in the collection, excluding the "ID" key
        """
        print("DietCollection: retrieving all diets:")
        diets_list = []
        for diet in self.diets.values():
            diet_without_id = diet.copy()  # Create a copy of the diet object
            del diet_without_id["ID"]  # Remove the "ID" key from the copied object
            diets_list.append(diet_without_id)
        print(diets_list)
        return diets_list

    def insertDiet(self, diet_name, cal, sodium, sugar):
        """
        Insert a new diet
        param: diet_name, cal, sodium, sugar
        return: id of the new diet (key) and status code
        """

        for id, diet in self.diets.items(): # check if diet exists, if so - return an error
            if diet["name"] == diet_name:
                print("Diet with name ", diet_name, " already exists")
                return 422

        self.opNum += 1  # increment latest operation number

        self.diet[self.opNum] = {
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


"""
The resources are:
- /diets or /diets{name}            Each diet resource is expressed with a specific JSON object
"""

# create DietsCollection instance with global scope
dietColl = DietCollection()

class Diets(Resource):
    """
    The Diets class implements the REST operations for the /diets resource
    /diets
        POST (add a diet of the given name)
        GET (return the JSON object listing all diets, indexed by ID)
    """

    global dietColl

    def get(self):
        """
        Retrieves all the diets from the collection
        :param key: None
        :return: JSON object and the status code
        """

        return dietColl.retrieveAllDiets(), 200

    def post(self):
        """
        Adds a diet to /diets given a JSON object with fields: name, cal, sodium, sugar
        :return: id: ID given to the created diet
        """
        # if request content-type is not application/json
        if 'Content-Type' not in dict(request.headers).keys():
            print("Request Content-Type not specified in header")
            return 0, 415
        else:
            if dict(request.headers)['Content-Type'] != "application/json":
                print("POST expects content type to be application/json")
                return 0, 415

        data = request.json # accept data as json

        # if body is not of type dict
        if type(data) != dict:
            return 0, 415
        else:
            # if name is empty or spelled wrong
            if ['name', 'cal', 'sodium', 'sugar'] != list(data.keys()):
                return -1, 422
            else:
                d = data['name']

        id = dietColl.insertDish(d, data['cal'], data['sodium'], data['sugar'])  # add diet to collection

        return id, 201

class DietsName(Resource):
    """ Implements the REST operations for the /diets/{name} resource
    /diets/{name}
    GET (return the JSON object of the diets given the name)
    """

    global dietColl

    def get(self, name):
        """ Retrieve a specific diet from the collection based off its name
        :param: the name of the diet to retrieve
        :return: the diet and the status code
        """

        (b, w) = dietColl.findDietName(name)
        if b:
            return w, 200  # return the diet and status code 200 ok
        else:
            return -5, 404  # return -5 for key and Not Found error code



