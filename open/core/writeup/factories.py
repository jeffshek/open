from factory.django import DjangoModelFactory

from open.core.models import WriteUpSharedPrompt


class WriteUpSharedPromptFactory(DjangoModelFactory):
    class Meta:
        model = WriteUpSharedPrompt
