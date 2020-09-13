from open.utilities.fields import create_django_choice_tuple_from_list

DEMO_TESTING_ACCOUNT = "demo-testing@senrigan.io"


class BetterSelfResourceConstants:
    """
    RESTful constants used in URLs, useful for URL lookups
    """

    MEASUREMENTS = "measurements"
    INGREDIENTS = "ingredients"
    INGREDIENT_COMPOSITIONS = "ingredient_compositions"
    SUPPLEMENTS = "supplements"
    FOODS = "foods"
    FOOD_LOGS = "food_logs"
    SUPPLEMENT_STACKS = "supplement_stacks"
    SUPPLEMENT_STACK_COMPOSITIONS = "supplement_stack_compositions"
    SUPPLEMENT_LOGS = "supplement_logs"
    DAILY_PRODUCTIVITY_LOGS = "productivity_logs"
    SLEEP_LOGS = "sleep_logs"
    ACTIVITIES = "activities"
    ACTIVITY_LOGS = "activity_logs"
    WELL_BEING_LOGS = "well_being_logs"
    OVERVIEW = "overview"
    DAILY_REVIEW = "daily_review"
    AGGREGATE = "aggregate"


WEB_INPUT_SOURCE = "web"
TEXT_MSG_SOURCE = "text_message"
API_INPUT_SOURCE = "api"

BETTERSELF_LOG_INPUT_SOURCES = [
    API_INPUT_SOURCE,
    "ios",
    "android",
    "mobile",
    WEB_INPUT_SOURCE,
    "user_excel",
    TEXT_MSG_SOURCE,
    "legacy_import",
]

INPUT_SOURCES_TUPLES = create_django_choice_tuple_from_list(
    BETTERSELF_LOG_INPUT_SOURCES
)


class BetterSelfFactoryConstants:
    # useful for generating fixtures
    DEFAULT_INGREDIENT_NAME_1 = "Leucine"
    DEFAULT_INGREDIENT_HL_MINUTE_1 = 50
    DEFAULT_INGREDIENT_DETAILS_1 = {
        "name": DEFAULT_INGREDIENT_NAME_1,
        "half_life_minutes": DEFAULT_INGREDIENT_HL_MINUTE_1,
    }

    DEFAULT_INGREDIENT_NAME_2 = "Valine"
    DEFAULT_INGREDIENT_HL_MINUTE_2 = 50
    DEFAULT_INGREDIENT_DETAILS_2 = {
        "name": DEFAULT_INGREDIENT_NAME_2,
        "half_life_minutes": DEFAULT_INGREDIENT_HL_MINUTE_2,
    }

    DEFAULT_INGREDIENT_NAME_3 = "Isoleucine"
    DEFAULT_INGREDIENT_HL_MINUTE_3 = 50
    DEFAULT_INGREDIENT_DETAILS_3 = {
        "name": DEFAULT_INGREDIENT_NAME_3,
        "half_life_minutes": DEFAULT_INGREDIENT_HL_MINUTE_3,
    }

    DEFAULT_MEASUREMENT_NAME = "milligram"
    DEFAULT_MEASUREMENT_SHORT_NAME = "mg"
    DEFAULT_MEASUREMENT_DETAILS = {
        "name": DEFAULT_INGREDIENT_NAME_1,
        "short_name": DEFAULT_MEASUREMENT_SHORT_NAME,
    }


class TEST_CONSTANTS:
    NAME_1 = "WOW"
    NOTES_1 = "ATE A CHEESEBURGER"

    NAME_2 = "SAD"
    NOTES_2 = "FELL DOWN STAIRS"
    NOTES_3 = "imma be productive and cure cancer"

    # a semantically correct uuid, but doesn't belong to anything
    INVALID_UUID = "d0acd6e3-41c4-45ac-a821-376aa273c40a"


PRODUCTIVITY_METRICS = [
    "very_productive_time_minutes",
    "productive_time_minutes",
    "neutral_time_minutes",
    "distracting_time_minutes",
    "very_distracting_time_minutes",
    "pomodoro_count",
]
