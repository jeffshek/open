from django.contrib import admin

from open.core.betterself.models.activity import Activity
from open.core.betterself.models.activity_log import ActivityLog
from open.core.betterself.models.daily_productivity_log import DailyProductivityLog
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


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "modified",
        "created",
        "uuid",
        "user",
        "notes",
        "name",
        "is_significant_activity",
        "is_negative_activity",
        "is_all_day_activity",
    )
    list_filter = (
        "modified",
        "created",
        "user",
        "is_significant_activity",
        "is_negative_activity",
        "is_all_day_activity",
    )
    search_fields = ("name",)


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "modified",
        "created",
        "uuid",
        "user",
        "notes",
        "activity",
        "source",
        "duration_minutes",
        "time",
    )
    list_filter = ("modified", "created", "user", "activity", "time")


@admin.register(DailyProductivityLog)
class DailyProductivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "modified",
        "created",
        "uuid",
        "user",
        "notes",
        "source",
        "date",
        "very_productive_time_minutes",
        "productive_time_minutes",
        "neutral_time_minutes",
        "distracting_time_minutes",
        "very_distracting_time_minutes",
    )
    list_filter = ("modified", "created", "user", "date")


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "modified",
        "created",
        "uuid",
        "user",
        "notes",
        "name",
        "half_life_minutes",
    )
    list_filter = ("modified", "created", "user")
    search_fields = ("name",)


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "modified",
        "created",
        "uuid",
        "name",
        "short_name",
        "is_liquid",
    )
    list_filter = ("modified", "created", "is_liquid")
    search_fields = ("name",)


@admin.register(IngredientComposition)
class IngredientCompositionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "modified",
        "created",
        "uuid",
        "user",
        "notes",
        "ingredient",
        "measurement",
        "quantity",
    )
    list_filter = (
        "modified",
        "created",
        "user",
        "ingredient",
        "measurement",
    )


@admin.register(SleepLog)
class SleepLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "modified",
        "created",
        "uuid",
        "user",
        "notes",
        "source",
        "start_time",
        "end_time",
    )
    list_filter = ("modified", "created", "user", "start_time", "end_time")


@admin.register(Supplement)
class SupplementAdmin(admin.ModelAdmin):
    list_display = (
        # "id",
        # "modified",
        # "created",
        # "uuid",
        "user",
        "notes",
        "name",
    )
    list_filter = ("modified", "created", "user")
    raw_id_fields = ("ingredient_compositions",)
    search_fields = ("name",)


@admin.register(SupplementLog)
class SupplementLogAdmin(admin.ModelAdmin):
    list_display = (
        # "id",
        # "modified",
        # "created",
        # "uuid",
        "time",
        "supplement",
        "user",
        "notes",
        # "source",
        "quantity",
    )
    # list_filter = ("supplement",)


@admin.register(SupplementStack)
class SupplementStackAdmin(admin.ModelAdmin):
    list_display = (
        # "id",
        # "modified",
        # "created",
        # "uuid",
        "user",
        "notes",
        "name",
    )
    # list_filter = ("modified", "created", "user")
    search_fields = ("name",)


@admin.register(SupplementStackComposition)
class SupplementStackCompositionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "modified",
        "created",
        "uuid",
        "user",
        "notes",
        "supplement",
        "stack",
        "quantity",
    )
    list_filter = ("modified", "created", "user", "supplement", "stack")


@admin.register(WellBeingLog)
class WellBeingLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "modified",
        "created",
        "uuid",
        "user",
        "notes",
        "time",
        "mental_value",
        "physical_value",
        "source",
    )
    list_filter = ("modified", "created", "user", "time")
