from factory.django import DjangoModelFactory

from open.core.writeup.models import (
    WriteUpPrompt,
    WriteUpPromptVote,
    WriteUpFlaggedPrompt,
)


class WriteUpPromptFactory(DjangoModelFactory):
    class Meta:
        model = WriteUpPrompt


class WriteUpPromptVoteFactory(DjangoModelFactory):
    class Meta:
        model = WriteUpPromptVote


class WriteUpFlaggedPromptFactory(DjangoModelFactory):
    class Meta:
        model = WriteUpFlaggedPrompt
