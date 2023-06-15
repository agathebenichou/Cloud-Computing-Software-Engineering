from flask import request
from flask_restful import Resource
from .collection import DietCollection

"""
The resources are:
- /diets                This is a collection class, containing all the old
- /diets/{name}         Each diet resource is expressed with a specific JSON object
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
        :return: ID given to the created diet
        """
        
        if request.headers is None:
            print("Request Content-Type not specified in header")
            return 0, 415

        if type(request.headers) != dict:
            print("Request Content-Type not specified in header")
            return 0, 415

        # if request content-type is not application/json
        if 'Content-Type' not in dict(request.headers).keys():
            print("Request Content-Type not specified in header")
            return "POST expects content type to be application/json", 415
        else:
            if dict(request.headers)['Content-Type'] != "application/json":
                return "POST expects content type to be application/json", 415

        data = request.json # accept data as json

        # if body is not of type dict
        if type(data) != dict:
            return 0, 415
        else:
            # if name is empty or spelled wrong
            if ['name', 'cal', 'sodium', 'sugar'] != list(data.keys()):
                return "Incorrect POST format", 422
            else:
                d = data['name']

        code = dietColl.insertDiet(d, data['cal'], data['sodium'], data['sugar'])  # add diet to collection
        if not code: # if it returns 0, then the diet already exists
            return f"Diet with {d} already exists", 422

        return f"Diet {d} was created successfully", 201


class DietsName(Resource):
    """ Implements the REST operations for the /diets/{name} resource
    /diets/{name}
    GET (return the JSON object of the diets given the name)
    """

    global dietColl

    def get(self, name):
        """ Retrieve a specific diet from the collection based on its name
        :param: the name of the diet to retrieve
        :return: the diet and the status code
        """

        (b, w) = dietColl.findDietName(name)
        if b:
            return w, 200  # return the diet and status code 200 ok
        else:
            return f"Diet {name} not found", 404
