from src.utils import capitalize, calculate_average, slugify, clamp, sort_students


# --- Tests capitalize ---
def test_should_capitalize_first_letter_when_lowercase_string():
    text = "hello"
    result = capitalize(text)
    assert result == "Hello"


def test_should_lowercase_other_letters_when_uppercase_string():
    text = "WORLD"
    result = capitalize(text)
    assert result == "World"


def test_should_return_empty_string_when_string_is_empty():
    text = ""
    result = capitalize(text)
    assert result == ""


def test_should_return_empty_string_when_input_is_none():
    text = None
    result = capitalize(text)
    assert result == ""


# --- Tests calculate_average ---
def test_should_calculate_average_when_valid_list_of_numbers():
    numbers = [10, 12, 14]
    result = calculate_average(numbers)
    assert result == 12


def test_should_return_same_number_when_single_element_list():
    numbers = [15]
    result = calculate_average(numbers)
    assert result == 15


def test_should_return_zero_when_list_is_empty():
    numbers = []
    result = calculate_average(numbers)
    assert result == 0


def test_should_return_zero_when_input_is_none():
    numbers = None
    result = calculate_average(numbers)
    assert result == 0


# --- Tests slugify ---
def test_should_format_slug_when_standard_text():
    text = "Hello World"
    result = slugify(text)
    assert result == "hello-world"


def test_should_trim_and_replace_spaces_when_extra_spaces():
    text = "  Spaces  Everywhere  "
    result = slugify(text)
    assert result == "spaces-everywhere"


def test_should_remove_special_chars_when_accented_string():
    text = "C'est l'ete !"
    result = slugify(text)
    assert result == "cest-lete"


def test_should_return_empty_string_when_slugify_empty_input():
    text = ""
    result = slugify(text)
    assert result == ""


# --- Tests clamp ---
def test_should_return_value_when_value_is_within_range():
    result = clamp(5, 0, 10)
    assert result == 5


def test_should_return_min_when_value_is_below_min():
    result = clamp(-5, 0, 10)
    assert result == 0


def test_should_return_max_when_value_is_above_max():
    result = clamp(15, 0, 10)
    assert result == 10


def test_should_return_zero_when_min_max_value_are_zero():
    result = clamp(0, 0, 0)
    assert result == 0


def test_should_sort_students_by_grade_ascending():
    from src.utils import sort_students
    students = [{"name": "Bob", "grade": 12}, {"name": "Alice", "grade": 18}]
    res = sort_students(students, sort_by="grade", order="asc")
    assert res[0]["name"] == "Bob"


def test_should_sort_students_by_grade_descending():
    students = [{"name": "Bob", "grade": 12}, {"name": "Alice", "grade": 18}]
    res = sort_students(students, sort_by="grade", order="desc")
    assert res[0]["name"] == "Alice"


def test_should_sort_students_by_name_ascending():
    students = [{"name": "Bob", "grade": 12}, {"name": "Alice", "grade": 18}]
    res = sort_students(students, sort_by="name", order="asc")
    assert res[0]["name"] == "Alice"


def test_should_return_empty_array_when_students_is_empty_or_none():
    assert sort_students([]) == []
    assert sort_students(None) == []


def test_should_not_modify_original_array_when_sorting():
    students = [{"name": "Bob", "grade": 12}, {"name": "Alice", "grade": 18}]
    sort_students(students, sort_by="grade", order="asc")
    assert students[0]["name"] == "Bob"
