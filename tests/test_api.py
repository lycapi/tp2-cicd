import pytest
from src.app import app, orders_db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    orders_db.clear()
    with app.test_client() as client:
        yield client


def test_should_return_200_when_simulation_is_successful(client):
    payload = {
        "items": [{"name": "Pizza", "price": 10.0, "quantity": 2}],
        "distance": 2.0,
        "weight": 1.0,
        "hour": 15,
        "dayOfWeek": "mardi",
    }
    res = client.post("/orders/simulate", json=payload)
    assert res.status_code == 200
    assert res.json["total"] == 22.0


def test_should_return_200_when_simulation_has_valid_promo(client):
    payload = {
        "items": [{"name": "Pizza", "price": 20.0, "quantity": 2}],
        "distance": 2.0,
        "weight": 1.0,
        "promoCode": "BIENVENUE20",
    }
    res = client.post("/orders/simulate", json=payload)
    assert res.status_code == 200
    assert res.json["discount"] == 8.0


def test_should_return_400_when_simulation_distance_exceeds_10km(client):
    payload = {"items": [{"name": "Pizza", "price": 10.0, "quantity": 1}], "distance": 15.0, "weight": 1.0}
    res = client.post("/orders/simulate", json=payload)
    assert res.status_code == 400


def test_should_return_400_when_simulation_restaurant_is_closed(client):
    payload = {"items": [{"name": "Pizza", "price": 10.0, "quantity": 1}], "distance": 2.0, "weight": 1.0, "hour": 23}
    res = client.post("/orders/simulate", json=payload)
    assert res.status_code == 400


def test_should_return_400_when_simulation_promo_code_has_expired(client):
    payload = {"items": [{"name": "Pizza", "price": 20.0, "quantity": 1}], "distance": 2.0, "weight": 1.0, "promoCode": "EXPIRE10"}
    res = client.post("/orders/simulate", json=payload)
    assert res.status_code == 400


def test_should_return_400_when_simulation_items_list_is_empty(client):
    res = client.post("/orders/simulate", json={"items": [], "distance": 2.0, "weight": 1.0})
    assert res.status_code == 400


def test_should_return_200_and_apply_weekend_surge_in_simulation(client):
    payload = {"items": [{"name": "Pizza", "price": 10.0, "quantity": 1}], "distance": 2.0, "weight": 1.0, "hour": 20, "dayOfWeek": "vendredi"}
    res = client.post("/orders/simulate", json=payload)
    assert res.status_code == 200
    assert res.json["surge"] == 1.8


def test_should_return_201_when_order_creation_succeeds(client):
    payload = {"items": [{"name": "Burger", "price": 12.0, "quantity": 1}], "distance": 1.0, "weight": 0.5}
    res = client.post("/orders", json=payload)
    assert res.status_code == 201
    assert "id" in res.json


def test_should_retrieve_created_order_by_id(client):
    payload = {"items": [{"name": "Burger", "price": 12.0, "quantity": 1}], "distance": 1.0, "weight": 0.5}
    post_res = client.post("/orders", json=payload)
    order_id = post_res.json["id"]

    get_res = client.get(f"/orders/{order_id}")
    assert get_res.status_code == 200
    assert get_res.json["id"] == order_id


def test_should_return_404_when_order_id_does_not_exist(client):
    res = client.get("/orders/9999")
    assert res.status_code == 404


def test_should_assign_distinct_ids_to_consecutive_orders(client):
    p = {"items": [{"name": "B", "price": 10.0, "quantity": 1}], "distance": 1.0, "weight": 0.5}
    r1 = client.post("/orders", json=p)
    r2 = client.post("/orders", json=p)
    assert r1.json["id"] != r2.json["id"]


def test_should_return_400_when_creating_invalid_order(client):
    res = client.post("/orders", json={"items": []})
    assert res.status_code == 400


def test_should_not_save_invalid_order_in_database(client):
    client.post("/orders", json={"items": []})
    assert len(orders_db) == 0


def test_should_verify_full_json_structure_of_retrieved_order(client):
    p = {"items": [{"name": "B", "price": 10.0, "quantity": 1}], "distance": 1.0, "weight": 0.5}
    post_res = client.post("/orders", json=p)
    order_id = post_res.json["id"]

    get_res = client.get(f"/orders/{order_id}")
    data = get_res.json
    assert "id" in data
    assert "items" in data
    assert "pricing" in data


def test_should_retrieve_second_order_independently(client):
    p1 = {"items": [{"name": "A", "price": 10.0, "quantity": 1}], "distance": 1.0, "weight": 0.5}
    p2 = {"items": [{"name": "B", "price": 20.0, "quantity": 1}], "distance": 1.0, "weight": 0.5}
    client.post("/orders", json=p1)
    r2 = client.post("/orders", json=p2)
    id2 = r2.json["id"]

    get_res = client.get(f"/orders/{id2}")
    assert get_res.status_code == 200
    assert get_res.json["pricing"]["subtotal"] == 20.0
