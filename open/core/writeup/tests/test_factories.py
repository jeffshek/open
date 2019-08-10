from test_plus import TestCase

from open.core.writeup.factories import (
    WriteUpPromptFactory,
    WriteUpPromptVoteFactory,
    WriteUpFlaggedPromptFactory,
)


class TestFactoryMixin:
    def test_factory(self):
        instance = self.FACTORY()
        self.assertIsNotNone(instance)


class TestWriteUpPromptFactories(TestCase, TestFactoryMixin):
    FACTORY = WriteUpPromptFactory

    def test_score_calculated(self):
        instance = self.FACTORY()
        self.assertTrue(instance.score != 0)

    def test_writeup_prompt_factory_loaded(self):
        text = "Jeff Was Here"
        email = "Jeff Was Here"
        title = "Jeff Was Here"

        writeup_prompt = WriteUpPromptFactory(text=text, email=email, title=title)

        self.assertEqual(writeup_prompt.text, text)
        self.assertEqual(writeup_prompt.email, text)
        self.assertEqual(writeup_prompt.title, text)


class TestWriteUpPromptVoteFactory(TestCase, TestFactoryMixin):
    FACTORY = WriteUpPromptVoteFactory


class TestWriteUpFlaggedPromptFactory(TestCase):
    FACTORY = WriteUpFlaggedPromptFactory
