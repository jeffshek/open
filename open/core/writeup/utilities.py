from open.core.writeup.constants import GPT2_END_TEXT_STRING


def serialize_gpt2_responses(text):
    text_serialized = text

    if GPT2_END_TEXT_STRING in text_serialized:
        end_location = text_serialized.index(GPT2_END_TEXT_STRING)
        text_serialized = text_serialized[:end_location]

    return text_serialized
