from open.core.writeup.constants import GPT2_END_TEXT_STRING


def serialize_text_algo_individual_values(text):
    """ Remove end of line and any other particular oddities you discover """
    text_serialized = text.strip()

    if GPT2_END_TEXT_STRING in text_serialized:
        end_location = text_serialized.index(GPT2_END_TEXT_STRING)
        text_serialized = text_serialized[:end_location]

    return text_serialized


def serialize_text_algo_api_response(returned_data):
    text_responses = returned_data.copy()
    for key, value in returned_data.items():
        if "text_" not in key:
            continue

        value_serialized = serialize_text_algo_individual_values(value)
        text_responses[key] = value_serialized

    return text_responses
