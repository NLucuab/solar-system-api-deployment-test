def test_create_one_planet(client):
    # Act
    response = client.post("/planets", json={
        "name": "ZigZag",
        "description": "A ziggy zaggy planet",
        "size": "Large"
        })
    response_body = response.get_json()
    
    # Assert 
    assert response.status_code == 201
    assert response_body['message'] == "Planet ZigZag successfully created"
    assert response_body['success'] == True

def test_get_one_planet(client, two_saved_planets):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert_planet(response_body)

def test_get_planet_by_name(client, two_saved_planets):
    # Act
    response = client.get("/planets", query_string={"name": "Swirly Planet"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert_planet(response_body[0])


def assert_planet(actual):
    assert actual["id"] == 1
    assert actual["name"] == "Swirly Planet"
    assert actual["description"] == "a swirl planet"
    assert actual["size"] == "Small"
