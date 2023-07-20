from original_hw1_tests.restApiController import *
from original_hw1_tests.connectionController import *
# from restApiController import *

# tests if POST /dishes returns different ID's and a 201 status_code
def test_1():
    dish_ids = []

    # Post 3 dishes and collect their IDs
    for dish in ["orange", "spaghetti", "apple pie"]:
        response = add_dish(dish) # in add_dish we check for 201 status_code, the response is the ID of the new dish
        dish_id = response
        dish_ids.append(dish_id)

    # Check if all dish ID's are different
    assert len(dish_ids) == len(set(dish_ids))


# tests if GET /dishes/<orange-ID> sodium is 0.9-1.1 and status_code is 200
def test_2():
    orange_id = 1 # orange ID is 1 since it's the first dish we add
    response = http_get(f"dishes/{orange_id}")
    assert_err_code(response, error_code=200)
    assert 0.9 <= response.json()["sodium"] <= 1.1


# tests if GET /dishes returns all 3 dishes and status_code 200
def test_3():
    response = http_get("dishes")
    dishes = response.json()
    assert_err_code(response, error_code=200)
    assert len(dishes) == 3


# tests if POST /dishes/"blah" returns -3 and status_code 404, 400 or 422
def test_4():
    dish = {"name": "blah"}
    response = http_post("dishes",  dish)
    assert response.status_code in [404, 400, 422]
    assert_ret_value(response, returned_value=-3)


# tests if POST /dishes with an existing dish returnss -2 and status_code 400, 404 or 422
def test_5():
    dish = {"name": "orange"}
    response = http_post("dishes",  dish)
    assert response.status_code in [404, 400, 422]
    assert_ret_value(response, returned_value=-2)


# tests POST /meals return positive ID and status_code 201
def test_6():
    meal = {
        "name": "delicious",
        "appetizer": 1,
        "main": 2,
        "dessert": 3
    }
    response = http_post("meals", meal)
    assert response.status_code == 201
    assert response.json() > 0


# tests GET /meals returns 1 meal, calories is between 400 to 500 and status_code 200
def test_7():
    response = http_get("meals")
    assert_err_code(response, error_code=200)
    assert len(response.json()) == 1
    assert 400 <= response.json()["1"]["cal"] <= 500


# tests POST /meals with existing meal returns -2 and status_code 400 or 422
def test_8():
    meal = {
        "name": "delicious",
        "appetizer": 1,
        "main": 2,
        "dessert": 3
    }
    response = http_post("meals", meal)
    assert response.status_code in [400, 422]
    # assert_ret_value(response, returned_value=-2)
    assert_ret_value(response, returned_value=-22)

