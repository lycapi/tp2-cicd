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

from src.pricing import apply_promo_code


def test_should_apply_percentage_discount_when_promo_is_valid():
    res = apply_promo_code(50.0, "BIENVENUE20")
    assert res["discount"] == 10.0
    assert res["new_subtotal"] == 40.0


def test_should_apply_fixed_discount_when_promo_is_valid():
    res = apply_promo_code(30.0, "REDUC5")
    assert res["discount"] == 5.0
    assert res["new_subtotal"] == 25.0


def test_should_return_no_discount_when_promo_code_is_none():
    res = apply_promo_code(30.0, None)
    assert res["discount"] == 0.0
    assert res["new_subtotal"] == 30.0


def test_should_return_no_discount_when_promo_code_is_empty_string():
    res = apply_promo_code(30.0, "")
    assert res["discount"] == 0.0
    assert res["new_subtotal"] == 30.0


def test_should_raise_error_when_promo_code_is_unknown():
    with pytest.raises(ValueError, match="invalide ou inconnu"):
        apply_promo_code(30.0, "CODE_INEXISTANT")


def test_should_raise_error_when_subtotal_is_below_minimum_order():
    with pytest.raises(ValueError, match="Commande minimum"):
        apply_promo_code(10.0, "BIENVENUE20")


def test_should_apply_promo_when_subtotal_equals_exact_minimum_order():
    res = apply_promo_code(15.0, "BIENVENUE20")
    assert res["discount"] == 3.0


def test_should_raise_error_when_promo_code_has_expired():
    with pytest.raises(ValueError, match="expiré"):
        apply_promo_code(20.0, "EXPIRE10")


def test_should_cap_discount_to_subtotal_if_discount_exceeds_price():
    custom_db = {"OFFRE_GEANTE": {"code": "OFFRE_GEANTE", "type": "fixed", "value": 100, "minOrder": 0, "expiresAt": "2026-12-31"}}
    res = apply_promo_code(20.0, "OFFRE_GEANTE", promo_codes_db=custom_db)
    assert res["discount"] == 20.0
    assert res["new_subtotal"] == 0.0


def test_should_raise_error_when_subtotal_is_negative_or_none():
    with pytest.raises(ValueError, match="positif"):
        apply_promo_code(-10.0, "REDUC5")
    with pytest.raises(ValueError, match="positif"):
        apply_promo_code(None, "REDUC5")


from src.pricing import calculate_surge


def test_should_return_normal_multiplier_during_regular_weekday_hours():
    assert calculate_surge(15, "mardi") == 1.0


def test_should_return_lunch_surge_on_weekdays():
    assert calculate_surge(12, "mardi") == 1.3


def test_should_return_dinner_surge_on_weekdays():
    assert calculate_surge(20, "jeudi") == 1.5


def test_should_return_weekend_night_surge():
    assert calculate_surge(20, "vendredi") == 1.8
    assert calculate_surge(21, "samedi") == 1.8


def test_should_return_sunday_surge():
    assert calculate_surge(14, "dimanche") == 1.2


def test_should_return_zero_surge_when_closed_at_night():
    assert calculate_surge(23, "lundi") == 0.0


def test_should_return_zero_surge_when_closed_early_morning():
    assert calculate_surge(8, "lundi") == 0.0


def test_should_handle_exact_opening_boundary_at_10am():
    assert calculate_surge(10, "lundi") == 1.0
