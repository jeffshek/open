from factory.django import DjangoModelFactory

from open.core.writeup.models import WriteUpSharedPrompt


class WriteUpSharedPromptFactory(DjangoModelFactory):
    class Meta:
        model = WriteUpSharedPrompt
