from restApiController import *

# tests if POST /dishes is valid (201 status_code and all have different IDs)
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
    response = connectionController.http_get(f"dishes/{orange_id}")
    assert_err_code(response, error_code=200)
    assert 0.9 <= response.json()["sodium"] <= 1.1

# tests if GET /dishes return all 3 dishes and status_code 200
def test_3():
    response = connectionController.http_get("dishes")
    dishes = response.json()
    assert_err_code(response, error_code=200)
    assert len(dishes) == 3

# tests if POST /dishes/"blah" return -3 and status code 404,400 or 422
def test_4():
    dish = {"name": "blah"}
    response = connectionController.http_post("dishes",  dish)
    assert response.status_code in [404, 400, 422]
    assert_ret_value(response, returned_value=-3)



