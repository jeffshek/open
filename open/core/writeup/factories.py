from factory.django import DjangoModelFactory

from open.core.writeup.models import WriteUpPrompt


class WriteUpSharedPromptFactory(DjangoModelFactory):
    class Meta:
        model = WriteUpPrompt
