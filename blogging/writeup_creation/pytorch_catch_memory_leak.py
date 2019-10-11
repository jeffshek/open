def get_process_prompt_response(request, validated_data):
    try:
        output = generate_sequences_from_prompt(**validated_data)
    except RuntimeError as exc:
        if "out of memory" in str(exc):
            logger.exception(
                f"Ran Out of Memory When Running {validated_data}. Clearing Cache."
            )
            torch.cuda.empty_cache()

            oom_response = get_oom_response(validated_data)
            return oom_response

    response = serialize_sequences_to_response(
        output,
        validated_data["prompt"],
        validated_data["cache_key"],
        WebsocketMessageTypes.COMPLETED_RESPONSE,
        completed=validated_data["length"],
        length=validated_data["length"],
    )

    # clear cache on all responses (maybe this is overkill)
    torch.cuda.empty_cache()
    return response
