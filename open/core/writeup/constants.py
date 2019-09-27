# to differentiate between finetuned models
ENGLISH_CONSTANT = "english"
GENERAL_CONSTANT = "general"

TEXT_GENERATION_URL = "text_generation"


class WriteUpResourceEndpoints:
    GENERATED_SENTENCE = "generated_sentence"
    PROMPTS = "prompts"
    PROMPT_VOTES = "prompt_votes"
    PROMPT_FLAGS = "prompt_flags"


GPT2_END_TEXT_STRING = "<|endoftext|>"


class TransformerXLNetTokenTypes:
    """
    AFAIK - Both XLNet and TransformersXL share the same type of tokens
    """

    BEGINNING_OF_PROMPT = "<s>"
    ENDING_OF_PROMPT = "</s>"
    ENDING_OF_PARAGRAPH = "<eop>"
    UNKNOWN_TOKEN = "<unk>"

    # not sure what the other tokens are supposed to do since i don't have wifi at the moment ...
    # TODO - Add tests to these when you figure it out
    SEPARATE_TOKEN = "<sep>"
    PADDING_TOKEN = "<pad>"
    CLS_TOKEN = "<cls>"

    # TODO - Debate if you want to implement this
    MASK_TOKEN = "<mask>"


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
    # GPT2_SMALL = "gpt2"
    GPT2_LARGE = "gpt2-large"
    # all the new self-generated
    # GPT2_SMALL_LEGAL = "gpt2-small-legal"
    GPT2_MEDIUM_LEGAL = "gpt2-medium-legal"
    GPT2_MEDIUM_HP = "gpt2-medium-hp"
    GPT2_MEDIUM_GOT = "gpt2-medium-got"
    GPT2_MEDIUM_RESEARCH = "gpt2-medium-research"
    GPT2_MEDIUM_LYRICS = "gpt2-medium-lyrics"
    GPT2_MEDIUM_COMPANIES = "gpt2-medium-companies"


ML_MODEL_NAME_CHOICES = [
    (MLModelNames.XLNET_LARGE_CASED, "XLNet Large Cased"),
    (MLModelNames.XLNET_BASE_CASED, "XLNet Base Cased"),
    # (MLModelNames.GPT2_SMALL, "GPT2 Small"),
    # (MLModelNames.GPT2_SMALL_LEGAL, "GPT2 Small Legal"),
    (MLModelNames.GPT2_MEDIUM, "GPT2 Medium"),
    (MLModelNames.GPT2_MEDIUM_LEGAL, "GPT2 Medium Legal"),
    (MLModelNames.GPT2_MEDIUM_HP, "GPT2 Medium HP"),
    (MLModelNames.GPT2_MEDIUM_GOT, "GPT2 Medium GOT"),
    (MLModelNames.GPT2_MEDIUM_RESEARCH, "GPT2 Medium Research"),
    (MLModelNames.GPT2_MEDIUM_LYRICS, "GPT2 Medium Lyrics"),
    (MLModelNames.GPT2_MEDIUM_COMPANIES, "GPT2 Medium Companies"),
    #
    (MLModelNames.GPT2_LARGE, "GPT2 Large"),
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


class WebsocketMessageTypes:
    NEW_REQUEST = "new_request"
    CANCEL_REQUEST = "cancel_request"
    UPDATED_RESPONSE = "updated_response"
    COMPLETED_RESPONSE = "completed_response"
