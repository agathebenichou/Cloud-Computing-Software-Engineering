from flask_restful import Resource, Api, reqparse

"""
The resources are:

- /meals                            This is a collection class, containing all the meals
- /meals/{ID} or /meals/{name}      Each meal resource is expressed with a specific JSON object
- /dishes                           This is a collection class, containing all the dishes 
- /dishes/{ID} or /dishes/{name}    Each dish resource is expressed with a specific JSON object

The supported operations on each of these resources are:

/meals
    POST (add a meal of the given name)
    GET (return the JSON object listing all meals, indexed by ID)
    
/meals/{ID}
    GET (return the JSON object of the meal given the ID)
    DELETE (delete a meal of the given ID)
    PUT (add a meal of the given ID)

/meals/{name}
    GET (return the JSON object of the meal given the name)
    DELETE (delete a meal of the given name)

/dishes
    POST (add a dish of the given name)
    GET (return the JSON object listing all dishes, indexed by ID)
    
/dishes/{ID} or /dishes/{name}
    GET (return the JSON object of the dish given the ID or name)
    DELETE (delete a dish of the given ID or name)

# ninja API key: 6zoIr+IoEg7H2GQGVDxw+g==WdtcKEIt1DOIoGKj
"""


# The Meal class implements the REST operations for the /meals resource
class Meal(Resource):
    pass


# The Dishes class implements the REST operations for the /dishes resource
class Dishes(Resource):
    pass


# The ID class implements the REST operations for the /dishes/{ID} or /meals/{ID} resource
class ID(Resource):
    pass


# The Name class implements the REST operations for the /dishes/{name} or /meals/{name} resource
class Name(Resource):
    pass
