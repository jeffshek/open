from django.contrib import admin

from open.core.writeup.models import (
    WriteUpPrompt,
    WriteUpPromptVote,
    WriteUpFlaggedPrompt,
)


@admin.register(WriteUpPrompt)
class WriteUpPromptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uuid",
        "text",
        "title",
        "user",
        "email",
        "instagram",
        "twitter",
        "website",
        "share_state",
        "staff_verified_share_state",
    )
    list_filter = ("user",)


@admin.register(WriteUpPromptVote)
class WriteUpPromptVoteAdmin(admin.ModelAdmin):
    list_display = ("uuid", "prompt", "user", "value")
    list_filter = ("prompt", "user")


@admin.register(WriteUpFlaggedPrompt)
class WriteUpFlaggedPromptAdmin(admin.ModelAdmin):
    list_display = ("id", "modified", "uuid", "prompt", "user")
    list_filter = ("prompt", "user")
