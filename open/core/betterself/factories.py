from factory import (
    DjangoModelFactory,
    LazyAttribute,
    SubFactory,
    LazyFunction,
    Faker,
    post_generation,
    SelfAttribute,
)
from factory.fuzzy import FuzzyInteger

from open.core.betterself.constants import API_INPUT_SOURCE
from open.core.betterself.models.activity import Activity
from open.core.betterself.models.activity_log import ActivityLog
from open.core.betterself.models.daily_productivity_log import DailyProductivityLog
from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.models.ingredient_composition import IngredientComposition
from open.core.betterself.models.measurement import Measurement
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.models.supplement_stack import SupplementStack
from open.core.betterself.models.supplement_stack_composition import (
    SupplementStackComposition,
)
from open.users.factories import UserFactory
from open.utilities.date_and_time import get_utc_now, get_utc_date


class IngredientFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    name = Faker("user_name")
    half_life_minutes = FuzzyInteger(1, 10)

    class Meta:
        model = Ingredient
        django_get_or_create = ("name", "user")


class MeasurementFactory(DjangoModelFactory):
    name = Faker("user_name")

    class Meta:
        model = Measurement
        django_get_or_create = ("name",)


class IngredientCompositionFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    ingredient = SubFactory(IngredientFactory)
    measurement = SubFactory(MeasurementFactory)
    quantity = FuzzyInteger(1, 10)

    class Meta:
        model = IngredientComposition


class SupplementFactory(DjangoModelFactory):
    name = Faker("user_name")
    user = SubFactory(UserFactory)
    notes = LazyAttribute(lambda obj: "%s notes" % obj.name)

    class Meta:
        model = Supplement
        django_get_or_create = ["name", "user"]

    @post_generation
    def ingredient_composition(self, create, extracted, **kwargs):
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

    class Meta:
        model = SupplementStack


class SupplementStackCompositionFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    # create the first user and pass it downwards
    supplement = SubFactory(
        SupplementFactory, user=LazyAttribute(lambda a: a.factory_parent.user)
    )
    stack = SubFactory(
        SupplementStackFactory, user=LazyAttribute(lambda a: a.factory_parent.user)
    )

    class Meta:
        model = SupplementStackComposition


class SupplementLogFactory(DjangoModelFactory):
    source = API_INPUT_SOURCE
    quantity = 1
    time = LazyFunction(get_utc_now)
    user = SubFactory(UserFactory)
    supplement = SubFactory(SupplementFactory)

    class Meta:
        model = SupplementLog


class DailyProductivityLogFactory(DjangoModelFactory):
    source = API_INPUT_SOURCE

    very_productive_time_minutes = FuzzyInteger(10, 30)
    productive_time_minutes = FuzzyInteger(10, 30)
    neutral_time_minutes = FuzzyInteger(10, 30)
    distracting_time_minutes = FuzzyInteger(10, 30)
    very_distracting_time_minutes = FuzzyInteger(10, 30)

    user = SubFactory(UserFactory)
    date = LazyFunction(get_utc_date)

    class Meta:
        model = DailyProductivityLog


class ActivityFactory(DjangoModelFactory):
    name = Faker("name")
    user = SubFactory(UserFactory)

    class Meta:
        model = Activity


class ActivityLogFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    time = LazyFunction(get_utc_now)
    activity = SubFactory(ActivityFactory, user=SelfAttribute("..user"))
    duration_minutes = FuzzyInteger(0, 100)

    class Meta:
        model = ActivityLog
