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
