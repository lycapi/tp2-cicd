import pytest
from src.pricing import calculate_delivery_fee


def test_should_return_base_fee_when_distance_under_3km_and_light_weight():
    assert calculate_delivery_fee(2.0, 1.0) == 2.00


def test_should_add_distance_surcharge_when_distance_exceeds_3km():
    assert calculate_delivery_fee(7.0, 3.0) == 4.00


def test_should_add_weight_surcharge_when_weight_exceeds_5kg():
    assert calculate_delivery_fee(2.0, 8.0) == 3.50


def test_should_calculate_exact_boundary_at_3km_and_5kg():
    assert calculate_delivery_fee(3.0, 5.0) == 2.00


def test_should_calculate_exact_boundary_at_10km_and_6kg():
    assert calculate_delivery_fee(10.0, 6.0) == 7.00


def test_should_raise_error_when_distance_exceeds_10km():
    with pytest.raises(ValueError, match="Livraison impossible"):
        calculate_delivery_fee(15.0, 2.0)


def test_should_raise_error_when_distance_or_weight_is_negative():
    with pytest.raises(ValueError, match="positifs"):
        calculate_delivery_fee(-1.0, 2.0)
    with pytest.raises(ValueError, match="positifs"):
        calculate_delivery_fee(2.0, -1.0)


def test_should_raise_error_when_distance_or_weight_is_none():
    with pytest.raises(ValueError, match="positifs"):
        calculate_delivery_fee(None, 2.0)
    with pytest.raises(ValueError, match="positifs"):
        calculate_delivery_fee(2.0, None)