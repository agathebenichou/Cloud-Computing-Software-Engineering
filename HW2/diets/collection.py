class DietCollection:
    """ DietCollection stores the old and performs operations on them
    Each diet is stored in a dictionary with a unique numerical key called id,
    and a value of the following: name, cal, sodium, sugar
    """

    def __init__(self):
        # self.opNum is the number of insertDiet operations performed, it also serves as the id for each diet
        self.opNum = 0

        # self.old is a dictionary of the form {key:diet} where key is an integer and diet is a JSON object
        self.diets = {}

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
