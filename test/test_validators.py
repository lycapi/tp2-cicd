from src.validators import is_valid_email, is_valid_password, is_valid_age


# --- Tests is_valid_email (7 tests) ---
def test_should_return_true_when_standard_valid_email():
    assert is_valid_email("user@example.com") is True


def test_should_return_true_when_email_has_subdomain_or_plus_tag():
    assert is_valid_email("user.name+tag@domain.co") is True


def test_should_return_false_when_email_has_no_at_symbol():
    assert is_valid_email("invalid") is False


def test_should_return_false_when_email_missing_username():
    assert is_valid_email("@domain.com") is False


def test_should_return_false_when_email_missing_domain():
    assert is_valid_email("user@") is False


def test_should_return_false_when_email_is_empty():
    assert is_valid_email("") is False


def test_should_return_false_when_email_is_none():
    assert is_valid_email(None) is False


# --- Tests is_valid_password (7 tests) ---
def test_should_return_valid_true_when_password_meets_all_rules():
    res = is_valid_password("Passw0rd!")
    assert res["valid"] is True
    assert res["errors"] == []


def test_should_return_errors_when_password_is_too_short():
    res = is_valid_password("short")
    assert res["valid"] is False
    assert "Au moins 8 caractères requis" in res["errors"]


def test_should_return_error_when_password_missing_uppercase():
    res = is_valid_password("alllowercase1!")
    assert res["valid"] is False
    assert "Au moins 1 majuscule requise" in res["errors"]


def test_should_return_error_when_password_missing_lowercase():
    res = is_valid_password("ALLUPPERCASE1!")
    assert res["valid"] is False
    assert "Au moins 1 minuscule requise" in res["errors"]


def test_should_return_error_when_password_missing_digit():
    res = is_valid_password("NoDigits!here")
    assert res["valid"] is False
    assert "Au moins 1 chiffre requis" in res["errors"]


def test_should_return_error_when_password_missing_special_character():
    res = is_valid_password("NoSpecial1here")
    assert res["valid"] is False
    assert "Au moins 1 caractère spécial requis" in res["errors"]


def test_should_return_invalid_when_password_is_empty_or_none():
    assert is_valid_password("")["valid"] is False
    assert is_valid_password(None)["valid"] is False


# --- Tests is_valid_age (8 tests) ---
def test_should_return_true_when_age_is_valid_integer():
    assert is_valid_age(25) is True


def test_should_return_true_when_age_is_lower_boundary_zero():
    assert is_valid_age(0) is True


def test_should_return_true_when_age_is_upper_boundary_150():
    assert is_valid_age(150) is True


def test_should_return_false_when_age_is_negative():
    assert is_valid_age(-1) is False


def test_should_return_false_when_age_exceeds_max():
    assert is_valid_age(151) is False


test_cases_invalid_age = [25.5, "25", None]


def test_should_return_false_when_age_type_is_invalid():
    for invalid_val in test_cases_invalid_age:
        assert is_valid_age(invalid_val) is False
