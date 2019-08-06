from test_plus import TestCase

from open.core.writeup.factories import (
    WriteUpPromptFactory,
    WriteUpPromptVoteFactory,
    WriteUpFlaggedPromptFactory,
)


class TestWriteUpPromptFactories(TestCase):
    def test_writeup_prompt_factory(self):
        writeup_prompt = WriteUpPromptFactory()
        self.assertIsNotNone(writeup_prompt)

    def test_writeup_prompt_factory_loaded(self):
        text = "Jeff Was Here"
        email = "Jeff Was Here"
        title = "Jeff Was Here"

        writeup_prompt = WriteUpPromptFactory(text=text, email=email, title=title)

        self.assertEqual(writeup_prompt.text, text)
        self.assertEqual(writeup_prompt.email, text)
        self.assertEqual(writeup_prompt.title, text)


class TestWriteUpPromptVoteFactory(TestCase):
    def test_factory(self):
        instance = WriteUpPromptVoteFactory()
        self.assertIsNotNone(instance)


class TestWriteUpFlaggedPromptFactory(TestCase):
    def test_factory(self):
        instance = WriteUpFlaggedPromptFactory()
        self.assertIsNotNone(instance)
