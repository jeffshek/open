from factory import SubFactory
from factory.django import DjangoModelFactory
from factory import Faker
from factory.fuzzy import FuzzyInteger

from open.core.writeup.models import (
    WriteUpPrompt,
    WriteUpPromptVote,
    WriteUpFlaggedPrompt,
)


class WriteUpPromptFactory(DjangoModelFactory):
    email = Faker("email")
    text = Faker("text")
    instagram = Faker("first_name")
    twitter = Faker("first_name")
    score = FuzzyInteger(1, 1000)

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
