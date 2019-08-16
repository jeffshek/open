import hashlib

from open.core.writeup.constants import MLModelNames


def get_cache_key_for_text_algo_parameter(
    prompt,
    batch_size,
    length,
    temperature,
    top_k,
    language="english_common",
    model_name=MLModelNames.GPT2_MEDIUM,
):
    app = "writeup"

    # have to encode into bytes first
    # just do this for redis's memory not to take up too much space
    # there's no speed difference in using shorter keys though, redis is too good
    prompt_encoded = prompt.strip().encode("utf-8")
    prompt_hash = hashlib.md5(prompt_encoded).hexdigest()

    cache_key = f"{app}_{prompt_hash}_{batch_size}_{length}_{temperature}_{top_k}_{language}_{model_name}"
    return cache_key


def get_cache_key_for_processing_algo_parameter(cache_key):
    # need a prefix, otherwise that's be cache collusion with data
    return f"processing_{cache_key}"
