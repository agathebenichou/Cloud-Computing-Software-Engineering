from assertions import *
from connectionController import http_post


def add_dish(name: str) -> int:
    dish = {"name": name}
    response = http_post("dishes", dish)
    assert_valid_added_resource(response)
    return response.json()


def add_meal(name: str, appetizer_id: int, main_id: int, dessert_id: int) -> int:
    meal = {
        "name": name,
        "appetizer": appetizer_id,
        "main": main_id,
        "dessert": dessert_id
    }
    response = http_post("meals", meal)
    assert_valid_added_resource(response)
    return response.json()
