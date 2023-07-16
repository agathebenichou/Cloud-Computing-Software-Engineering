# from original_hw1_tests import connectionController, assertions

from original_hw1_tests.assertions import *
from original_hw1_tests.restApiController import *


# tests if POST /dishes is valid (201 status_code and all have different IDs)
def test_1():
    dish_ids = []

    # Post 3 dishes and collect their IDs
    for dish in ["orange", "spaghetti", "apple pie"]:
        response = add_dish(dish) # in add_dish we check for 201 status_code, the response is of type json
        dish_id = response["ID"]
        dish_ids.append(dish_id)

    # Check if all dish ID's are different
    assert len(dish_ids) == len(set(dish_ids))


# tests if GET /dishes/<orange-ID> sodium is 0.9-1.1 and status_code is 200
def test_2():
    orange_id = add_dish("orange")
    response = connectionController.http_get(f"dishes/{orange_id}")
    assert_err_code(response, error_code=200)
    assert 0.9 <= response.json()["sodium"] <= 1.1
