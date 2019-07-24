import hashlib


def get_cache_key_for_gpt2_parameter(
    prompt, batch_size, length, temperature, top_k, language="english_common"
):
    app = "writeup"

    # have to encode into bytes first
    # just do this for redis's memory not to take up too much space
    # there's no speed difference in using shorter keys though, redis is too good
    prompt_encoded = prompt.strip().encode("utf-8")
    prompt_hash = hashlib.md5(prompt_encoded).hexdigest()

    cache_key = (
        f"{app}_{prompt_hash}_{batch_size}_{length}_{temperature}_{top_k}_{language}"
    )
    return cache_key
