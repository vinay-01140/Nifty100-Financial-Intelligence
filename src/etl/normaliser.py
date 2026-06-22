import re


def normalize_ticker(value):
    if value is None:
        return None

    value = str(value).strip().upper()

    value = value.replace(".NS", "")
    value = value.replace(".BO", "")

    # remove internal extra spaces/newlines/tabs
    value = value.replace("\n", "")
    value = value.replace("\t", "")
    value = re.sub(r"\s+", "", value)

    return value


def normalize_year(year_value):
    """
    Convert financial year labels into a standard year.

    Examples:
    Mar 2024    -> 2024
    Dec 2023    -> 2023
    Sep 2024    -> 2024
    Mar 2016 9m -> 2016
    Mar 2023 15 -> 2023
    TTM         -> None
    """

    if year_value is None:
        return None

    year_value = str(year_value).strip()

    if year_value.upper() == "TTM":
        return None

    match = re.search(r"(20\d{2})", year_value)

    if match:
        return int(match.group(1))

    return None