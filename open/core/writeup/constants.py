class WriteUpResourceEndpoints:
    GENERATED_SENTENCE = "generated_sentence"
    PROMPTS = "prompts"
    PROMPT_VOTES = "prompt_votes"
    PROMPT_FLAGS = "prompt_flags"


GPT2_END_TEXT_STRING = "<|endoftext|>"


class MLModelTypes:
    GPT2 = "gpt2"
    XLNET = "xlnet"
    TRANSFORMER_XL = "transfo-xl"


ML_MODEL_TYPE_CHOICES = [
    (MLModelTypes.GPT2, "GPT2"),
    (MLModelTypes.TRANSFORMER_XL, "TransformerXL"),
    (MLModelTypes.XLNET, "XLNet"),
]


class MLModelNames:
    # mimic how huggingface calls it!
    XLNET_BASE_CASED = "xlnet-base-cased"
    XLNET_LARGE_CASED = "xlnet-large-cased"
    GPT2_MEDIUM = "gpt2-medium"
    TRANSFO_XL_WT103 = "transfo-xl-wt103"


ML_MODEL_NAME_CHOICES = [
    (MLModelNames.XLNET_LARGE_CASED, "XLNet Large Cased"),
    (MLModelNames.XLNET_BASE_CASED, "XLNet Base Cased"),
    (MLModelNames.GPT2_MEDIUM, "GPT2 Medium"),
    # robots in disguise ...
    (MLModelNames.TRANSFO_XL_WT103, "Transformer XL WT 103"),
]


class StaffVerifiedShareStates:
    # admin would review any unverified issues and if they're bad
    # put them as fail and just not show them
    VERIFIED_FAIL = "verified_fail"
    VERIFIED_PASS = "verified_pass"
    # when someone marks something as bad, put this into this state
    # if something has been reported multiple times (more than 3), change
    # the state to more likely bad
    UNVERIFIED_ISSUE_MULTIPLE = "unverified_issue_multiple"
    UNVERIFIED_ISSUE = "unverified_issue"
    UNVERIFIED = "unverified"


# everything else means it's failed
SHOWABLE_STAFF_VERIFIED_STATES = [
    StaffVerifiedShareStates.VERIFIED_PASS,
    StaffVerifiedShareStates.UNVERIFIED_ISSUE,
    StaffVerifiedShareStates.UNVERIFIED,
]

STAFF_VERIFIED_SHARE_STATE_CHOICES = [
    (StaffVerifiedShareStates.VERIFIED_FAIL, "Verified Fail"),
    (StaffVerifiedShareStates.VERIFIED_PASS, "Verified Pass"),
    # the default state is unverified, shouldn't have to review most things
    # but when something is reported as an issue, put it in here
    (StaffVerifiedShareStates.UNVERIFIED_ISSUE_MULTIPLE, "Unverified Issue Multiple"),
    (StaffVerifiedShareStates.UNVERIFIED_ISSUE, "Unverified Issue"),
    (StaffVerifiedShareStates.UNVERIFIED, "Unverified"),
]


class PromptShareStates:
    UNSHARED = "unshared"
    # access only if you have special link
    PUBLISHED_LINK_ACCESS_ONLY = "published_link_access_only"
    # everyone has access, let people search and find, show on ranking
    PUBLISHED = "published"


PROMPT_SHARE_STATES_CHOICES = [
    (PromptShareStates.UNSHARED, "Unshared"),
    (PromptShareStates.PUBLISHED_LINK_ACCESS_ONLY, "Link Access Only"),
    (PromptShareStates.PUBLISHED, "Published"),
]
