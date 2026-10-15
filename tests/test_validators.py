from src.validators import is_valid_email, is_valid_password, is_valid_age


# ==============================================================================
# TESTS : is_valid_email (7 tests)
# ==============================================================================

def test_should_return_true_when_standard_valid_email():
    # Arrange
    email = "user@example.com"
    # Act
    result = is_valid_email(email)
    # Assert
    assert result is True


def test_should_return_true_when_email_has_subdomain_or_plus_tag():
    # Arrange
    email = "user.name+tag@domain.co"
    # Act
    result = is_valid_email(email)
    # Assert
    assert result is True


def test_should_return_false_when_email_has_no_at_symbol():
    # Arrange
    email = "invalid"
    # Act
    result = is_valid_email(email)
    # Assert
    assert result is False


def test_should_return_false_when_email_missing_username():
    # Arrange
    email = "@domain.com"
    # Act
    result = is_valid_email(email)
    # Assert
    assert result is False


def test_should_return_false_when_email_missing_domain():
    # Arrange
    email = "user@"
    # Act
    result = is_valid_email(email)
    # Assert
    assert result is False


def test_should_return_false_when_email_is_empty():
    # Arrange
    email = ""
    # Act
    result = is_valid_email(email)
    # Assert
    assert result is False


def test_should_return_false_when_email_is_none():
    # Arrange
    email = None
    # Act
    result = is_valid_email(email)
    # Assert
    assert result is False


# ==============================================================================
# TESTS : is_valid_password (7 tests)
# ==============================================================================

def test_should_return_valid_true_when_password_meets_all_rules():
    # Arrange
    pwd = "Passw0rd!"
    # Act
    result = is_valid_password(pwd)
    # Assert
    assert result["valid"] is True
    assert result["errors"] == []


def test_should_return_errors_when_password_is_too_short():
    # Arrange
    pwd = "short"
    # Act
    result = is_valid_password(pwd)
    # Assert
    assert result["valid"] is False
    assert "Au moins 8 caractères requis" in result["errors"]


def test_should_return_error_when_password_missing_uppercase():
    # Arrange
    pwd = "alllowercase1!"
    # Act
    result = is_valid_password(pwd)
    # Assert
    assert result["valid"] is False
    assert "Au moins 1 majuscule requise" in result["errors"]


def test_should_return_error_when_password_missing_lowercase():
    # Arrange
    pwd = "ALLUPPERCASE1!"
    # Act
    result = is_valid_password(pwd)
    # Assert
    assert result["valid"] is False
    assert "Au moins 1 minuscule requise" in result["errors"]


def test_should_return_error_when_password_missing_digit():
    # Arrange
    pwd = "NoDigits!here"
    # Act
    result = is_valid_password(pwd)
    # Assert
    assert result["valid"] is False
    assert "Au moins 1 chiffre requis" in result["errors"]


def test_should_return_error_when_password_missing_special_character():
    # Arrange
    pwd = "NoSpecial1here"
    # Act
    result = is_valid_password(pwd)
    # Assert
    assert result["valid"] is False
    assert "Au moins 1 caractère spécial requis" in result["errors"]


def test_should_return_invalid_when_password_is_empty_or_none():
    # Arrange & Act
    res_empty = is_valid_password("")
    res_none = is_valid_password(None)
    # Assert
    assert res_empty["valid"] is False
    assert res_none["valid"] is False


# ==============================================================================
# TESTS : is_valid_age (8 tests)
# ==============================================================================

def test_should_return_true_when_age_is_valid_integer():
    # Arrange
    age = 25
    # Act
    result = is_valid_age(age)
    # Assert
    assert result is True


def test_should_return_true_when_age_is_lower_boundary_zero():
    # Arrange
    age = 0
    # Act
    result = is_valid_age(age)
    # Assert
    assert result is True


def test_should_return_true_when_age_is_upper_boundary_150():
    # Arrange
    age = 150
    # Act
    result = is_valid_age(age)
    # Assert
    assert result is True


def test_should_return_false_when_age_is_negative():
    # Arrange
    age = -1
    # Act
    result = is_valid_age(age)
    # Assert
    assert result is False


def test_should_return_false_when_age_exceeds_max():
    # Arrange
    age = 151
    # Act
    result = is_valid_age(age)
    # Assert
    assert result is False


def test_should_return_false_when_age_is_float():
    # Arrange
    age = 25.5
    # Act
    result = is_valid_age(age)
    # Assert
    assert result is False


def test_should_return_false_when_age_is_string():
    # Arrange
    age = "25"
    # Act
    result = is_valid_age(age)
    # Assert
    assert result is False


def test_should_return_false_when_age_is_none():
    # Arrange
    age = None
    # Act
    result = is_valid_age(age)
    # Assert
    assert result is False
