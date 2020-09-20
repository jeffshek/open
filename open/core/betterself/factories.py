import random

from factory import (
    DjangoModelFactory,
    LazyAttribute,
    SubFactory,
    LazyFunction,
    Faker,
    post_generation,
    SelfAttribute,
)
from factory.fuzzy import FuzzyInteger, FuzzyDate, FuzzyDateTime, FuzzyChoice

from open.core.betterself.constants import API_INPUT_SOURCE
from open.core.betterself.fixtures.supplement_fixtures import (
    SUPPLEMENT_FIXTURES_NAME_AND_NOTES,
)
from open.core.betterself.models.activity import Activity
from open.core.betterself.models.activity_log import ActivityLog
from open.core.betterself.models.daily_productivity_log import DailyProductivityLog
from open.core.betterself.models.food import Food
from open.core.betterself.models.food_logs import FoodLog
from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.models.ingredient_composition import IngredientComposition
from open.core.betterself.models.measurement import Measurement
from open.core.betterself.models.sleep_log import SleepLog
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.models.supplement_stack import SupplementStack
from open.core.betterself.models.supplement_stack_composition import (
    SupplementStackComposition,
)
from open.core.betterself.models.well_being_log import WellBeingLog
from open.core.betterself.fixtures.demo_constants import (
    FOOD_NAMES,
    ACTIVITY_NAMES,
    NOTES_TO_USE_WITH_EMPTY_SPACES,
    PRODUCTIVITY_NOTES_TO_USE,
)
from open.users.factories import UserFactory
from open.utilities.date_and_time import (
    get_utc_date_relative_units_ago,
    get_utc_time_relative_units_ago,
    get_time_relative_units_ago,
)


def get_supplement_name():
    options = list(SUPPLEMENT_FIXTURES_NAME_AND_NOTES.keys())
    selected_supplement_name = random.choice(options)
    return selected_supplement_name

    # # add a random 2 digit number to make it more random
    # two_random_digits = random.randint(10, 99)
    #
    # serialized_name = f"{selected_supplement_name}{two_random_digits}"
    #
    # return serialized_name


def get_supplement_notes(instance):
    # go all the way to the last two, since those codes are randomly generated
    # original_supplement_name = instance.name[:-2]

    return SUPPLEMENT_FIXTURES_NAME_AND_NOTES.get(instance.name, "Details Don't Exist")


class IngredientFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    name = LazyFunction(get_supplement_name)
    notes = LazyAttribute(lambda a: get_supplement_notes(a))
    half_life_minutes = FuzzyInteger(1, 10)

    class Meta:
        model = Ingredient
        django_get_or_create = ("name", "user")


class MeasurementFactory(DjangoModelFactory):
    name = Faker("user_name")
    short_name = FuzzyChoice(["mL", "g", "kg", "mg"])

    class Meta:
        model = Measurement
        django_get_or_create = ("name",)


class IngredientCompositionFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    ingredient = SubFactory(IngredientFactory)
    measurement = SubFactory(MeasurementFactory)
    quantity = FuzzyInteger(1, 10)
    notes = FuzzyChoice(NOTES_TO_USE_WITH_EMPTY_SPACES)

    class Meta:
        model = IngredientComposition


class SupplementFactory(DjangoModelFactory):
    name = LazyFunction(get_supplement_name)
    user = SubFactory(UserFactory)
    notes = LazyAttribute(lambda a: get_supplement_notes(a))

    class Meta:
        model = Supplement
        django_get_or_create = ["name", "user"]

    @post_generation
    def ingredient_compositions(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.ingredient_compositions.add(group)


class SupplementStackFactory(DjangoModelFactory):
    name = Faker("user_name")
    user = SubFactory(UserFactory)
    notes = FuzzyChoice(NOTES_TO_USE_WITH_EMPTY_SPACES)

    class Meta:
        model = SupplementStack
        django_get_or_create = ["user", "name"]


class SupplementStackCompositionFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    # create the first user and pass it downwards
    supplement = SubFactory(
        SupplementFactory, user=LazyAttribute(lambda a: a.factory_parent.user)
    )
    stack = SubFactory(
        SupplementStackFactory, user=LazyAttribute(lambda a: a.factory_parent.user)
    )
    notes = FuzzyChoice(NOTES_TO_USE_WITH_EMPTY_SPACES)

    class Meta:
        model = SupplementStackComposition
        django_get_or_create = ["user", "supplement", "stack"]


class SupplementLogFactory(DjangoModelFactory):
    source = API_INPUT_SOURCE
    quantity = FuzzyInteger(1, 3)
    time = FuzzyDateTime(start_dt=get_utc_time_relative_units_ago(years=1))
    user = SubFactory(UserFactory)
    supplement = SubFactory(SupplementFactory)
    notes = FuzzyChoice(NOTES_TO_USE_WITH_EMPTY_SPACES)

    class Meta:
        model = SupplementLog
        django_get_or_create = ["user", "time", "supplement"]


class DailyProductivityLogFactory(DjangoModelFactory):
    source = API_INPUT_SOURCE

    very_productive_time_minutes = FuzzyInteger(10, 30)
    productive_time_minutes = FuzzyInteger(10, 30)
    neutral_time_minutes = FuzzyInteger(10, 30)
    distracting_time_minutes = FuzzyInteger(10, 30)
    very_distracting_time_minutes = FuzzyInteger(10, 30)
    pomodoro_count = FuzzyInteger(0, 15)

    user = SubFactory(UserFactory)
    date = FuzzyDate(start_date=get_utc_date_relative_units_ago(years=2))

    notes = FuzzyChoice(PRODUCTIVITY_NOTES_TO_USE)

    class Meta:
        model = DailyProductivityLog
        # this causes a problem i don't entirely understand why
        # factory.errors.FactoryError: django_get_or_create - Unable to find initialization value for 'user, date' in factory DailyProductivityLogFactory
        django_get_or_create = ["user", "date"]


class ActivityFactory(DjangoModelFactory):
    name = FuzzyChoice(ACTIVITY_NAMES)
    user = SubFactory(UserFactory)
    notes = FuzzyChoice(NOTES_TO_USE_WITH_EMPTY_SPACES)

    class Meta:
        model = Activity
        django_get_or_create = ["user", "name"]


class ActivityLogFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    time = FuzzyDateTime(start_dt=get_utc_time_relative_units_ago(years=2))
    activity = SubFactory(ActivityFactory, user=SelfAttribute("..user"))
    duration_minutes = FuzzyInteger(0, 100)
    notes = FuzzyChoice(NOTES_TO_USE_WITH_EMPTY_SPACES)

    class Meta:
        model = ActivityLog
        django_get_or_create = ["user", "activity", "time"]


class WellBeingLogFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    time = FuzzyDateTime(start_dt=get_utc_time_relative_units_ago(years=2))
    mental_value = FuzzyInteger(4, 10)
    physical_value = FuzzyInteger(4, 10)
    notes = FuzzyChoice(NOTES_TO_USE_WITH_EMPTY_SPACES)

    class Meta:
        model = WellBeingLog
        django_get_or_create = ["user", "time"]


def sleep_start_time(sleep_end_time):
    random_minutes = random.randint(1, 30)
    start_time = get_time_relative_units_ago(
        sleep_end_time, hours=8, minutes=random_minutes
    )
    return start_time


class SleepLogFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    start_time = LazyAttribute(lambda instance: sleep_start_time(instance.end_time))
    end_time = FuzzyDateTime(start_dt=get_utc_time_relative_units_ago(years=4))
    notes = FuzzyChoice(NOTES_TO_USE_WITH_EMPTY_SPACES)

    class Meta:
        model = SleepLog
        django_get_or_create = ["user", "start_time", "end_time"]


class FoodFactory(DjangoModelFactory):
    name = FuzzyChoice(FOOD_NAMES)
    user = SubFactory(UserFactory)
    notes = FuzzyChoice(NOTES_TO_USE_WITH_EMPTY_SPACES)

    class Meta:
        model = Food
        django_get_or_create = ["name", "user"]


class FoodLogFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    time = FuzzyDateTime(start_dt=get_utc_time_relative_units_ago(years=2))
    food = SubFactory(FoodFactory, user=SelfAttribute("..user"))
    quantity = FuzzyInteger(1, 10)
    notes = FuzzyChoice(NOTES_TO_USE_WITH_EMPTY_SPACES)

    class Meta:
        model = FoodLog
        django_get_or_create = ["user", "food", "time"]
