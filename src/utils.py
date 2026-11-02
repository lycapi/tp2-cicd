import re


def capitalize(str_val):
    if not str_val:
        return ""
    return str_val.capitalize()


def calculate_average(numbers):
    if not numbers:
        return 0
    return round(sum(numbers) / len(numbers), 2)


def slugify(text):
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

