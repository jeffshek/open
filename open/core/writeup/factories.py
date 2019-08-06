from factory.django import DjangoModelFactory

from open.core.writeup.models import WriteUpPrompt


class WriteUpPromptFactory(DjangoModelFactory):
    class Meta:
        model = WriteUpPrompt
