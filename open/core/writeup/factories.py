from factory import SubFactory
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
    prompt = SubFactory(WriteUpPromptFactory)

    class Meta:
        model = WriteUpPromptVote


class WriteUpFlaggedPromptFactory(DjangoModelFactory):
    prompt = SubFactory(WriteUpPromptFactory)

    class Meta:
        model = WriteUpFlaggedPrompt
