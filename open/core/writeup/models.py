from django.db.models import TextField, ForeignKey, SET_NULL, CASCADE, IntegerField
from django_extensions.db.fields.json import JSONField
from django_fsm import FSMField

from open.core.writeup.constants import (
    STAFF_VERIFIED_SHARE_STATE_CHOICES,
    StaffVerifiedShareStates,
    PROMPT_SHARE_STATES_CHOICES,
    PromptShareStates,
)
from open.users.models import User
from open.utilities.models import BaseModel


class WriteUpPrompt(BaseModel):
    text = TextField(default="", blank=True)
    content = JSONField(blank=True)
    title = TextField(default="", blank=True)
    user = ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
    # published/sharing options
    # let the writers/composers be famous, if they want other people
    # to contact them for good writing, allow them to put in their details
    email = TextField(default="", blank=True)
    instagram = TextField(default="", blank=True)
    twitter = TextField(default="", blank=True)
    website = TextField(default="", blank=True)
    # default to unshared, but allow people to share otherwise
    share_state = FSMField(
        choices=PROMPT_SHARE_STATES_CHOICES, default=PromptShareStates.UNSHARED
    )
    # catch bad/mean prompts that shouldn't be shown for things on the public list
    staff_verified_share_state = FSMField(
        choices=STAFF_VERIFIED_SHARE_STATE_CHOICES,
        default=StaffVerifiedShareStates.UNVERIFIED,
    )
    # this is a denormalized field that is the sum of all the upvotes
    # this serves as a quick queryable field, where it's also easy to easy
    # to recompute for all prompts when cpu is idle
    score = IntegerField(default=0)

    class Meta:
        verbose_name = "Write Up Prompt"

    def __str__(self):
        return f"{self.title} - {self.id}"


class WriteUpPromptVote(BaseModel):
    prompt = ForeignKey(WriteUpPrompt, on_delete=CASCADE)
    user = ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
    # values can be negative (up to -1), which means a downvote
    value = IntegerField(default=1)

    class Meta:
        unique_together = ("prompt", "user")
        verbose_name = "Write Up Prompt Vote"


class WriteUpFlaggedPrompt(BaseModel):
    # allow prompts that are public to be flagged
    # save who flagged it to prevent abuse
    prompt = ForeignKey(WriteUpPrompt, null=False, on_delete=CASCADE)
    user = ForeignKey(User, null=True, blank=True, on_delete=CASCADE)

    class Meta:
        unique_together = ("prompt", "user")
        verbose_name = "Write Up Flagged Prompt"
